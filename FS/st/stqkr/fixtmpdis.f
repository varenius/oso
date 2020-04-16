      subroutine fixtmpdis(ip,iclcm)
C  fixtmp display <880922.1238>
C 
C 1.1.   fixtmp displays the current wx temperature value
C 
C     INPUT VARIABLES:
      dimension ip(1) 
C        IP(1)  - class number of buffer from MATCN 
C        IP(2)  - # records in class
C        IP(3)  - error return from MATCN 
C        IP(4)  - who, or o'77' (?) 
C        IP(5)  - class with command
C 
C     OUTPUT VARIABLES: 
C        IP(1) - error
C        IP(2) - class
C        IP(3) - number of records
C        IP(4) - who we are 
C 
C 2.2.   COMMON BLOCKS USED 
      include '../../fs/include/fscom.i'
C 
C 2.5.   SUBROUTINE INTERFACE:
C     CALLED SUBROUTINES: character utilities 
C 
C 3.  LOCAL VARIABLES 
C
      integer*2 ibuf2(30) 
      dimension lfr(3)
      dimension ireg(2) 
      real extbw
      integer get_buf
C               - registers from EXEC 
      equivalence (reg,ireg(1)) 
C 
C 5.  INITIALIZED VARIABLES 
      data ilen/40/,ilen2/60/ 
C 
C 6.  PROGRAMMER: NRV 
C     LAST MODIFIED:   790216 
C 
C     PROGRAM STRUCTURE 
C 
C     1. Determine whether parameters from COMMON wanted and skip to
C     response section. 
C     Get RMPAR parameters and check for errors from our I/O request. 
C 
      if (iclcm.eq.0) return
C 
C     2. Get class buffer with command in it.  Set up first part
C     of output buffer.  Get first buffer from MATCN. 
C 
      ireg(2) = get_buf(iclcm,ibuf2,-ilen2,idum,idum)
C 
      nchar = ireg(2) 
      nch = iscn_ch(ibuf2,1,nchar,'=')
      if (nch.eq.0) nch = nchar+1 
C                   If no "=" found, position after last character
      nch = ichmv_ch(ibuf2,nch,'/') 
C                   Put / to indicate a response
C 
      call fs_get_tempwx(tempwx)
      nch = nch + ir2as(tempwx,ibuf2,nch,6,1)
C                   temperature C
C 
C 
C     5. Now send the buffer to SAM and schedule PPT. 
C 
      iclass = 0
      nch = nch - 1 
      call put_buf(iclass,ibuf2,-nch,'fs','  ')
C                   Send buffer starting with fmptmp/ for display.
      ierr = 0 
C 
      ip(1) = iclass
      ip(2) = 1 
      ip(3) = ierr
      call char2hol('st',ip(4),1,2)
      ip(5) = 0 

      return
      end 
