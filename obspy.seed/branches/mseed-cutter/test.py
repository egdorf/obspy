#!/usr/bin/python

import ctypes as C

lib = C.CDLL('./libmseed.so')

# SEED binary time
class BTime(C.Structure):
    _fields_ = [
        ('year', C.c_uint),
        ('day', C.c_uint),
        ('hour', C.c_ushort),
        ('min', C.c_ushort),
        ('sec', C.c_ushort),
        ('unused', C.c_ushort),
        ('fract', C.c_uint),
    ]


# Fixed section data of header
class fsdh_s(C.Structure):
    _fields_ = [
        ('sequence_number', C.c_char*6),
        ('dataquality', C.c_char),
        ('reserved', C.c_char), 
        ('station', C.c_char*5), 
        ('location', C.c_char*2), 
        ('channel', C.c_char*3), 
        ('network', C.c_char*2), 
        ('start_time', BTime),
        ('numsamples', C.c_uint), 
        ('samprate_fact', C.c_int), 
        ('samprate_mult', C.c_int), 
        ('act_flags', C.c_ushort), 
        ('io_flags', C.c_ushort), 
        ('dq_flags', C.c_ushort), 
        ('numblockettes', C.c_ushort), 
        ('time_correct', C.c_long), 
        ('data_offset', C.c_uint), 
        ('blockette_offset', C.c_uint), 
    ]


# Blockette 100, Sample Rate (without header)
class blkt_100_s(C.Structure):
    _fields_ = [
        ('samprate', C.c_float), 
        ('flags', C.c_short), 
        ('reserved', C.c_ushort*3), 
    ]


# Blockette 1000, Data Only SEED (without header)
class blkt_1000_s(C.Structure):
    _fields_ = [
        ('encoding', C.c_ushort), 
        ('byteorder', C.c_ushort), 
        ('reclen', C.c_ushort), 
        ('reserved', C.c_ushort),
    ]

# Blockette 1001, Data Extension (without header)
class blkt_1001_s(C.Structure):
    _fields_ = [
        ('timing_qual', C.c_ushort), 
        ('usec', C.c_short), 
        ('reserved', C.c_ushort), 
        ('framecnt', C.c_ushort),
    ]


# Blockette chain link, generic linkable blockette index
class blkt_link_s(C.Structure):
    pass
    
# incomplete type has to be defined this way 
blkt_link_s._fields_ = [
    ('blkt_type', C.c_uint),        # Blockette type
    ('next_blkt', C.c_uint),        # Offset to next blockette
    ('blktdata', C.c_void_p),       # Blockette data
    ('blktdatalen', C.c_uint),      # Length of blockette data in bytes
    ('next', C.POINTER(blkt_link_s)), 
]
BlktLink = blkt_link_s


class StreamState_s(C.Structure):
    _fields_ = [
        ('packedrecords', C.c_longlong), # Count of packed records
        ('packedsamples', C.c_longlong), # Count of packed samples
        ('lastintsample', C.c_long),     # Value of last integer sample packed
        ('comphistory', C.c_short),      # Control use of lastintsample for compression history
    ]
StreamState = StreamState_s


class MSRecord(C.Structure):
    _fields_ = [
        ('record', C.c_char_p),                 # Mini-SEED record
        ('reclen', C.c_int),                    # Length of Mini-SEED record in bytes
        # Pointers to SEED data record structures
        ('fsdh', C.POINTER(fsdh_s)),            # Fixed Section of Data Header
        ('blkts', C.POINTER(BlktLink)),         # Root of blockette chain
        ('Blkt100', C.POINTER(blkt_100_s)),     # Blockette 100, if present 
        ('Blkt1000', C.POINTER(blkt_1000_s)),   # Blockette 1000, if present
        ('Blkt1001', C.POINTER(blkt_1001_s)),   # Blockette 1001, if present
        # Common header fields in accessible form
        ('sequence_number', C.c_long),          # SEED record sequence number
        ('dataquality', C.c_char),              # Data quality indicator
        ('network', C.c_char*11),               # Network designation, NULL terminated
        ('station', C.c_char*11),               # Station designation, NULL terminated
        ('location', C.c_char*11),              # Location designation, NULL terminated
        ('channel', C.c_char*11),               # Channel designation, NULL terminated
        ('starttime', C.c_longlong),            # Record start time, corrected (first sample)
        ('samprate', C.c_double),               # Nominal sample rate (Hz)
        ('samplecnt', C.c_long),                # Number of samples in record
        ('encoding', C.c_short),                # Data encoding format
        ('byteorder', C.c_short),               # Byte order of record
        # Data sample fields
        ('datasamples', C.c_void_p),            # Data samples, 'numsamples' of type 'sampletype'
        ('numsamples', C.c_long),               # Number of data samples in datasamples
        ('sampletype', C.c_char),               # Sample type code: a, i, f, d
        # Stream oriented state information
        ('ststate', C.POINTER(StreamState)),    # Stream processing state information
    ]


class MSTrace_s(C.Structure):
    pass

MSTrace_s._fields_ = [
    ('network', C.c_char*11),               # Network designation, NULL terminated
    ('station', C.c_char*11),               # Station designation, NULL terminated
    ('location', C.c_char*11),              # Location designation, NULL terminated
    ('channel', C.c_char*11),               # Channel designation, NULL terminated
    ('dataquality', C.c_char),              # Data quality indicator
    ('type', C.c_char),                     # MSTrace type code
    ('starttime', C.c_longlong),            # Time of first sample
    ('endtime', C.c_longlong),              # Time of last sample
    ('samprate', C.c_double),               # Nominal sample rate (Hz
    ('samplecnt', C.c_long),                # Number of samples in trace coverage
    ('datasamples', C.c_void_p),            # Data samples, 'numsamples' of type 'sampletype'
    ('numsamples', C.c_long),               # Number of data samples in datasamples
    ('sampletype', C.c_char),               # Sample type code: a, i, f, d 
    ('prvtptr', C.c_void_p),                # Private pointer for general use
    ('ststate', C.POINTER(StreamState)),    # Stream processing state information
    ('next', C.POINTER(MSTrace_s)),         # Pointer to next trace
]
MSTrace = MSTrace_s


class MSTraceGroup_s(C.Structure):
    pass

MSTraceGroup_s._fields_ = [
    ('numtraces', C.c_long),                # Number of MSTraces in the trace chain
    ('traces', C.POINTER(MSTrace_s)),       # Root of the trace chain
]
MSTraceGroup = MSTraceGroup_s


msr = MSRecord()
while True:
   netstat=lib.ms_readmsr(C.pointer(msr), 'BW.BGLD..EHE.D.2008.001', 0, None, None, 1, 0, False)
   if netstat!=0:
       break
   lib.msr_print(msr, 0)
   import pdb
   pdb.set_trace()
print "here"
