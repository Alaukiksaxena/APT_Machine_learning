# -*- coding: utf-8 -*-
"""
Reader for the APSuite6/IVAS4 *.APT file format
MK::GPLV3, 03/09/2020, Markus K\"uhbach, m.kuehbach@mpie.de
"""


import numpy as np


#https://www.python-kurs.eu/numpy_dtype.php
class APTFileBranches():
    def __init__(self):
        self.dict_kwnsect = { 1: 'tof', 2: 'pulse', 3: 'freq', 4: 'tElapsed', 5: 'erate', 6: 'tstage', 7: 'TargetErate',
                         8: 'TargetFlux', 9: 'pulseDelta', 10: 'Pres', 11: 'VAnodeMon', 12: 'Temp', 13: 'AmbTemp', 14: 'FractureGuard',
                         15: 'Vref', 16: 'Noise', 17: 'Uniformity', 18: 'xstage', 19: 'ystage', 20: 'zstage', 21: 'z', 22: 'tofc', 23: 'Mass', 24: 'tofb',
                         25: 'xs', 26: 'ys', 27: 'zs', 28: 'rTip', 29: 'zApex', 30: 'zSphereCorr', 31: 'XDet_mm', 32: 'YDet_mm', 33: 'Multiplicity',
                         34: 'Vap', 35: 'Detector Coordinates', 36: 'Position'}
        
        self.dict_sectionid = { 'Failure': 0, 
                                'tof': 1, 'pulse': 2, 'freq': 3, 'tElapsed': 4, 'erate': 5, 'tstage': 6, 'TargetErate': 7,
                                'TargetFlux': 8, 'pulseDelta': 9, 'Pres': 10, 'VAnodeMon': 11, 'Temp': 12, 'AmbTemp': 13, 'FractureGuard': 14,
                                'Vref': 15, 'Noise': 16, 'Uniformity': 17, 'xstage': 18, 'ystage': 19, 'zstage': 20, 'z': 21, 'tofc': 22, 'Mass': 23, 'tofb': 24,
                                'xs': 25, 'ys': 26, 'zs': 27, 'rTip': 28, 'zApex': 29, 'zSphereCorr': 30, 'XDet_mm': 31, 'YDet_mm': 32, 'Multiplicity': 33,
                                'Vap': 34, 'Detector Coordinates': 35, 'Position': 36 }
                        
        self.dict_iHeaderSize = { 1: 148, 2: 148, 3: 148, 4: 148, 5: 148, 6: 148, 7: 148,
                             8: 148, 9: 148, 10: 148, 11: 148, 12: 148, 13: 148, 14: 148, 
                             15: 148, 16: 148, 17: 148, 18: 148, 19: 148, 20: 148, 21: 148, 22: 148, 23: 148, 24: 148, 
                             25: 148, 26: 148, 27: 148, 28: 148, 29: 148, 30: 148, 31: 148, 32: 148, 33: 148, 
                             34: 148, 35: 148, 36: 148+6*4 }

        self.dict_iHeaderVersion = { 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 
                                8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 
                                15: 2, 16: 2, 17: 2, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2, 
                                25: 2, 26: 2, 27: 2, 28: 2, 29: 2, 30: 2, 31: 2, 32: 2, 33: 2, 
                                34: 2, 35: 2, 36: 2 }

        self.dict_iSectionVersion = { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 
                                 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 
                                 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 
                                 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 
                                 34: 1, 35: 1, 36: 1 }

        self.dict_eRelationshipType = { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 
                                 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 
                                 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 
                                 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 
                                 34: 1, 35: 1, 36: 1 }

        self.dict_eRecordType = { 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 
                                 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 
                                 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 
                                 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 
                                 34: 1, 35: 1, 36: 1 }

        self.dict_eRecordDataType = { 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 3, 
                                 8: 3, 9: 1, 10: 3, 11: 3, 12: 3, 13: 3, 14: 2,
                                 15: 3, 16: 3, 17: 3, 18: 1, 19: 1, 20: 1,  21: 1, 22: 3, 23: 3, 24: 3, 
                                 25: 3, 26: 3, 27: 3, 28: 3, 29: 3, 30: 3, 31: 3, 32: 3, 33: 1, 
                                 34: 3, 35: 3, 36: 3}

        self.dict_iDataTypeSize = { 1: 32, 2: 32, 3: 32, 4: 32, 5: 32, 6: 16, 7: 32, 
                               8: 32, 9: 16, 10: 32, 11: 32, 12: 32, 13: 32, 14: 16, 
                               15: 32, 16: 32, 17: 32, 18: 32, 19: 32, 20: 32, 21: 64, 22: 32, 23: 32, 24: 32, 
                               25: 32, 26: 32, 27: 32, 28: 32, 29: 32, 30: 32, 31: 32, 32: 32, 33: 32, 
                               34: 32, 35: 32, 36: 32 }

        self.dict_iRecordSize = { 1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 2, 7: 4, 
                             8: 4, 9: 2, 10: 4, 11: 4, 12: 4, 13: 4, 14: 2, 
                             15: 4, 16: 4, 17: 4, 18: 4, 19: 4, 20: 4, 21: 8, 22: 4, 23: 4, 24: 4, 
                             25: 4, 26: 4, 27: 4, 28: 4, 29: 4, 30: 4, 31: 4, 32: 4, 33: 4, 
                             34: 4, 35: 8, 36: 12 }

        self.dict_iElements = dict()
        for i in range(1,len(self.dict_kwnsect)+1):
            self.dict_iElements[i] = int(self.dict_iRecordSize[i] / (self.dict_iDataTypeSize[i]/8))


class APTFileHeader():
    def __init__(self, fn, *args, **kwargs):
        self.known_sections = APTFileBranches()
        self.healthy = True
        self.aptfn = fn
        self.cSignature = ""
        self.iHeaderSize = 0
        self.iHeaderVersion = 0
        self.wcFilename = ""
        self.ftCreationTime = 0
        self.llIonCount = 0

    def read_cameca_apt_file_header(self, fid):
        ht = np.dtype([('cSignature', np.int8, (4,)),
               ('iHeaderSize', np.int32),
               ('iHeaderVersion', np.int32),
               ('wcFilename', np.uint16, 256),               
               ('ftCreationTime', np.uint64),
               ('llIonCount', np.uint64)])
        tmp = np.fromfile( fid , ht, count = 1 )  #unicode_, 256),
        str_parse = ""
        for i in tmp['cSignature'].flatten():
            if chr(i) != '\x00':
                str_parse = str_parse + chr(i)
        self.cSignature = str_parse
        if self.cSignature != 'APT':
           # print('The file header indicates the file is not a valid *.APT file!')
            self.healthy = False
            return None
        self.iHeaderSize = tmp['iHeaderSize'].flatten()[0]
        if self.iHeaderSize != 540:
        #    print('The iHeaderSize is unexpectedly different!')
            self.healthy = False
            return None
        self.iHeaderVersion = tmp['iHeaderVersion'].flatten()[0]
        if self.iHeaderVersion != 2:
         #   print('The iHeaderVersion is not 2 but only 2 is supported by this implementation!')
            self.healthy = False
            return None
        ###MK::parsing UTF-16 works currently only for the lower bit, for the 
        #APTV2 draft specification this is not a problem because currently the internal 
        ##section identifiers use only UTF-8 characters
        str_parse = ""
        for i in tmp['wcFilename'].flatten():
            if chr(i) != '\x00':
                str_parse = str_parse + chr(i)
        self.wcFilename = str_parse
        self.ftCreationTime = tmp['ftCreationTime'].flatten()[0]
        self.llIonCount = tmp['llIonCount'].flatten()[0]
        if self.llIonCount < 1:
       #     print('llIonCount < 1 means there are no ions in the dataset which is weird!')
            self.healthy = False
            return None
       # print('*.APT file ' + self.aptfn + ' successfully read ' + str(self.llIonCount) + ' ions')
        tmp = []
        str_parse = ""

    def print(self):
        print('APTFileHeader')
        print('healthy ' + str(self.healthy))
        print('aptfn ' + self.aptfn)
        print('cSignature ' + self.cSignature)
        print('iHeaderSize ' + str(self.iHeaderSize))
        print('iHeaderVersion ' + str(self.iHeaderVersion))
        print('wcFilename ' + self.wcFilename)
        print('ftCreationTime ' + str(self.ftCreationTime))
        print('llIonCount ' + str(self.llIonCount))
    
    #def get_offset(self):
    #    return 540
        
        
class APTSectionHeader():
    def __init__(self, *args, **kwargs): #fn
        self.healthy = True
        self.known_sections = APTFileBranches()
        #self.aptfn = fn
        self.cSignature = ""
        self.iHeaderSize = 0
        self.iHeaderVersion = 0
        self.wcSectionType = ""
        self.iSectionVersion = 0
        self.eRelationshipType = 0
        self.eRecordType = 0
        self.eRecordDataType = 0
        self.iDataTypeSize = 0
        self.iRecordSize = 0
        self.wcDataUnit = ""
        self.llRecordCount = 0
        self.llByteCount = 0

    def read_cameca_apt_section_header_auto(self, fid ):
        ht = np.dtype([('cSignature', np.int8, (4,)),
                       ('iHeaderSize', np.int32),
                       ('iHeaderVersion', np.int32),
                       ('wcSectionType', np.uint16, 32),
                       ('iSectionVersion', np.int32),
                       ('eRelationshipType', np.uint32),
                       ('eRecordType', np.uint32),
                       ('eRecordDataType', np.uint32),
                       ('iDataTypeSize', np.int32),
                       ('iRecordSize', np.int32),
                       ('wcDataUnit', np.uint16, 16),
                       ('llRecordCount', np.uint64),
                       ('llByteCount', np.uint64)])
        #skip the APTFileHeader and start reading the first section
        #f = open( self.aptfn, "rb" )
        #f.seek(offset, os.SEEK_SET) #seek set is relative to beginning of the file 
        tmp = np.fromfile( fid , ht, count = 1 )  #unicode_, 256),
        str_parse = ""
        for i in tmp['cSignature'].flatten():
            if chr(i) != '\x00':
                str_parse = str_parse + chr(i)
        self.cSignature = str_parse
        if self.cSignature != 'SEC':
          #  print('The section header is faulty, it misses the required SEC keyword!')
            self.healthy = False
            return None         
        ###MK::parsing UTF-16 works currently only for the lower bit, for the 
        #APTV2 draft specification this is not a problem because currently the internal 
        ##section identifiers use only UTF-8 characters
        str_parse = ""
        for i in tmp['wcSectionType'].flatten():
            if chr(i) != '\x00':
                str_parse = str_parse + chr(i)
        self.wcSectionType = str_parse
    #    print('__' + self.wcSectionType + '__')
        sectionid = self.known_sections.dict_sectionid.get(self.wcSectionType)
        if sectionid == None:
         #   print('Encountering an unknown section!')
            self.healthy = False
            return None
        ###MK::here HeaderSize and Version tested after reading wcSectionType
        self.iHeaderSize = tmp['iHeaderSize'].flatten()[0]
        if self.iHeaderSize != self.known_sections.dict_iHeaderSize[sectionid]:
         #   print('iHeaderSize is ' + str(self.iHeaderSize) + ' this does not match the expectation!')
            self.healthy = False
            return None
        self.iHeaderVersion = tmp['iHeaderVersion'].flatten()[0]
        if self.iHeaderVersion != self.known_sections.dict_iHeaderVersion[sectionid]:
         #   print('iHeaderVersion is ' + str(self.iHeaderVersion) + ' this does not match the expectation!')
            self.healthy = False
            return None

        self.iSectionVersion = tmp['iSectionVersion'].flatten()[0]
        if self.iSectionVersion != self.known_sections.dict_iSectionVersion[sectionid]:
         #   print('iSectionVersion is ' + str(self.iSectionVersion) + ' this does not match the expectation!')
            self.healthy = False
            return None
        self.eRelationshipType = tmp['eRelationshipType'].flatten()[0]
        if self.eRelationshipType != self.known_sections.dict_eRelationshipType[sectionid]:
         #   print('eRelationshipType is ' + str(self.eRelationshipType) + ' this does not match the expectation!')
            self.healthy = False
            return None
        self.eRecordType = tmp['eRecordType'].flatten()[0]
        if self.eRecordType != self.known_sections.dict_eRecordType[sectionid]:
         #   print('eRecordType is ' + str(self.eRecordType) + ' this does not match the expectation!')
            self.healthy = False
            return None
        self.eRecordDataType = tmp['eRecordDataType'].flatten()[0]
        if self.eRecordDataType != self.known_sections.dict_eRecordDataType[sectionid]:
         #   print('eRecordDataType is ' + str(self.eRecordDataType) + ' this does not match the expectation!')
            self.healthy = False
            return None
        self.iDataTypeSize = tmp['iDataTypeSize'].flatten()[0]
        if self.iDataTypeSize != self.known_sections.dict_iDataTypeSize[sectionid]:
         #   print('iDataTypeSize is ' + str(self.iDataTypeSize) + ' this does not match the expectation!')
            self.healthy = False
            return None
        self.iRecordSize = tmp['iRecordSize'].flatten()[0]
        if self.iRecordSize != self.known_sections.dict_iRecordSize[sectionid]:
         #   print('iRecordSize is ' + str(self.iRecordSize) + ' this does not match the expectation!')
            self.healthy = False
            return None
        str_parse = ""
        for i in tmp['wcDataUnit'].flatten():
            if chr(i) != '\x00':
                str_parse = str_parse + chr(i)
        self.wcDataUnit = str_parse
        self.llRecordCount = tmp['llRecordCount'].flatten()[0]
        ##MK::test implementatio remaining
        self.llByteCount = tmp['llByteCount'].flatten()[0]
     #   print('*.APT file successfully read ' + str(sectionid) + ' section header')
        tmp = []
        str_parse = ""
        ##MK::implement checks
        
    def print(self):
        print('APTSectionHeader')
        #print(self.aptfn)
        print('cSignature ' + self.cSignature)
        print('iHeaderSize ' + str(self.iHeaderSize))
        print('iHeaderVersion ' + str(self.iHeaderVersion))
        print('wcSectionType ' + self.wcSectionType)
        print('iSectionVersion ' + str(self.iSectionVersion))
        print('eRelationshipType ' + str(self.eRelationshipType))
        print('eRecordType ' + str(self.eRecordType))
        print('eRecordDataType ' + str(self.eRecordDataType))
        print('iDataTypeSize ' + str(self.iDataTypeSize))
        print('iRecordSize ' + str(self.iRecordSize))
        print('wcDataUnit ' + self.wcDataUnit)
        print('llRecordCount ' + str(self.llRecordCount))
        print('llByteCount ' + str(self.llByteCount))

    #def get_offset(self):
    #    if self.wcSectionType == "Position":
    #        return 148 #(148+6*4)
    #    else:
    #        return 148


class paraprobe_transcoder():
    
    def __init__(self, aptfn, *args, **kwargs):
        self.fn = aptfn
        self.filestream = None
        self.header = APTFileHeader( self.fn )
        self.idtfyd_sections = []
        #self.mass_sect = APTSectionHeader( self.fn )
        #self.xyz_sect = APTSectionHeader( self.fn )
    
    def read_cameca_apt_section_data_fixed_onetoone(self, fid, sect ):
        #which datatype to use, interpret from the section header
        ni = int(self.header.llIonCount)
    #    print('ni ' + str(ni))
        nj = int(int(sect.iRecordSize) / (int(sect.iDataTypeSize)/int(8)))
    #    print('nj ' + str(nj))
        dtyp = None #eRecordDataType == 3 and iDataTypeSize == 32
        if sect.eRecordDataType == 1:
            if sect.iDataTypeSize/8 == 2:
                dtyp = np.int16
            elif sect.iDataTypeSize/8 == 4:
                dtyp = np.int32
            elif sect.iDataTypeSize/8 == 8:
                dtyp = np.int64
            else:
       #         print('Unknown datatype selection!')
                return None
        elif sect.eRecordDataType == 2:
            ###MK::currently only one type used uint16
            dtyp = np.uint16
        elif sect.eRecordDataType == 3:
            dtyp = np.float32
        else:
       #     print('Unknown datatype selection!')
            return None        
   #     print(dtyp)
        return np.reshape(np.fromfile(fid, dtyp, count = int(ni*nj)), (int(ni), int(nj)), order='C')


    def read_cameca_apt(self):
        offset = 0
  #      print('Offset is ' + str(offset))
        
        self.filestream = open(self.fn, "rb")
        
        self.header.read_cameca_apt_file_header( self.filestream )
   #     self.header.print()

        #'Failure' is sectionid so one more keys, currently 36+1
        for sectionid in range(1,len(self.header.known_sections.dict_sectionid)):
            sect = APTSectionHeader()
            sect.read_cameca_apt_section_header_auto( self.filestream )
     #       sect.print()
        
            if sect.healthy == True:
                #read data of the section
                #large switch  #####
                #what type of section is this?
                sectionid = self.header.known_sections.dict_sectionid.get(sect.wcSectionType, 0) #0 is for 'Failure'#
       #         print('sectionid ' + str(sectionid))
                
                self.idtfyd_sections.append( sect )
                ###MK implement more elegantly using switchers
                #MK::here we use the fact that the file pointer gets advanced implicitly so after reading the sect it points to the 
                #first byte of the data section corresponding to the data associated with this section
                #this works because *.APT files by definition have the data following immediately after each section headers
                #with ##MK::at least as of 2020/03/20 no gaps in the binary structure
                if sectionid == 1:
                    self.tof = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect ) 
                elif sectionid == 2:
                    self.pulse = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 3:
                    self.freq = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 4:
                    self.tElapsed = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 5:
                    self.erate = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 6:
                    self.tstage = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 7:
                    self.TargetErate = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 8:
                    self.TargetFlux = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 9:
                    self.pulseDelta = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 10:
                     self.Pres = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 11:
                     self.VAnodeMon = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 12:
                     self.Temp = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 13:
                     self.AmbTemp = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 14:
                     self.FractureGuard = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 15:
                     self.Vref = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 16:
                     self.Noise = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 17:
                     self.Uniformity = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 18:
                     self.xstage = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 19:
                     self.ystage = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 20:
                     self.zstage = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 21:
                     self.z = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 22:
                     self.tofc = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 23:
                     self.Mass = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 24:
                     self.tofb = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 25:
                     self.xs = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 26:
                     self.ys = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 27:
                     self.zs = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 28:
                     self.rTip = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 29:
                     self.zApex = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 30:
                     self.zSphereCorr = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 31:
                     self.XDet_mm = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 32:
                     self.YDet_mm = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 33:
                     self.Multiplicity = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 34:
                     self.Vap = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 35:
                     self.DetectorCoordinates = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                elif sectionid == 36:
                     #position has preceeding 6 float32 for bounds
                     self.tipbox = np.reshape(np.fromfile( self.filestream, np.float32, count = int(2*3) ), (int(2), int(3) ), order='C')
                     self.Position = self.read_cameca_apt_section_data_fixed_onetoone( self.filestream, sect )
                else:
        #            print('Section is faulty, which is why we stop reading!')
                    self.filestream.close()
                    break
            else:
        #        print('Reached the end of the file!')
                self.filestream.close()
                break

        #done with all I/O on the *.APT file so close it
        self.filestream.close()
        print('Done, reading *.APT file')

#        self.header.read_cameca_apt_file_header()
#        offset = offset + self.header.get_offset()
#        print('Offset is ' + str(offset))

#        self.mass_sect.read_cameca_apt_section_header( offset )
#        offset = offset + self.mass_sect.get_offset()
#        print('Offset is ' + str(offset))
#
#        #load mass
#        f = open(self.fn, "rb")
#        f.seek(offset, os.SEEK_SET)
#        self.mq = []
#        self.mq = np.fromfile(f, np.float32, count = int(self.header.llIonCount)*1)
#        offset = offset + int(self.header.llIonCount) * 1 * 4
#        print('Offset is ' + str(offset))
#        print('Mass data read successfully!')
#        print(np.shape(self.mq))
#        
#        self.xyz_sect.read_cameca_apt_section_header( offset )
#        offset = offset + self.mass_sect.get_offset()
#        print('Offset is ' + str(offset))
#        #read x,y,z limits
#        f = open(self.fn, "rb")
#        f.seek(offset, os.SEEK_SET)
#        self.tipbox = np.fromfile(f, np.float32, count = 6)
#        offset = offset + 6*4
#        print('Offset is ' + str(offset))
#        #read x,y,z coordinates
#        f = open(self.fn, "rb")
#        f.seek(offset, os.SEEK_SET)
#        self.xyz = []
#        self.xyz = np.reshape(np.fromfile(f, np.float32, count = int(self.header.llIonCount)*3),
#                     (int(self.header.llIonCount),3), order='C')
#        print('Position coordinates read successfully')
#        print(np.shape(self.xyz))
#        offset = offset + int(self.header.llIonCount)*3*4
#        print('Offset is ' + str(offset))


#    def write(self, file_name: str):
#         #file_path = Path(file_name)
#         #file_path.write_text(self.to_utf8())
#         with open(file_name,'w') as f:
#             f.write(self.xml)


#example how to read a APT file from APSuite6/IVAS4
#minimal example with default output currently implemented after reconstruction wizard from APSuite6/IVAS4

#Tk().withdraw()
#fn = askopenfilename()
#maximal example with all branches of an *.APT file exported, be careful --- in APSuite6/IVAS4 this is super slow (40min for 8mio atoms! below)
#fn = 'Z:/GITHUB/MPIE_APTFIM_TOOLBOX/paraprobe/code/481f2262-b0d5-4dfb-91b7-fb31b57cd1b0.apt'
#apt = paraprobe_transcoder( fn )
#apt.read_cameca_apt()


#np.shape(apt.Mass)
#verbose
#apt.header.print()
#apt.mass_sect.print()
#apt.xyz_sect.print()
