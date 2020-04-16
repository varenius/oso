      subroutine fixtmp(ip,itask)
C 
C   fixmtp allows manual wx temperature definition for onsala
C         for caltemp at 22 GHZVC controls the video converters
C 
C     INPUT VARIABLES:
C 
      dimension ip(1) 
C        IP(1)  - class number of input parameter buffer
C        IP(2-5)- not used
C 
C     OUTPUT VARIABLES: 
C 
C        IP(1) - CLASS
C        IP(2) - # RECS 
C        IP(3) - ERROR
C        IP(4) - who we are 
C 
C 2.2.   COMMON BLOCKS USED 
C 
      include '../../fs/include/fscom.i'
C 
C 2.5.   SUBROUTINE INTERFACE:
C 
C     CALLING SUBROUTINES:
C 
C     CALLED SUBROUTINES: GTPRM
C 
C 3.  LOCAL VARIABLES 
C 
C        FREQ   - frequency specified, must be < 500MHz 
C        IBW    - bandwidth code
C        ITP    - TP code 
C        IATN   - attenuator code 
C        NCHAR  - number of characters in uffer 
C        ICH    - character counter 
      integer*2 ibuf(20)
C               - class buffer
      integer*2 lfr(3)
C        ILEN   - length of IBUF, chars 
      dimension iparm(2)
C               - parameters returned from GTPRM
      dimension ia(2) 
C               - attenuator settings 
      dimension ireg(2) 
      integer get_buf
C               - registers from EXEC calls 
      dimension lhex(15)
C               - hex characters corresponding to 1 - 14. 
C 
      character cjchar
      integer*4 il
      equivalence (reg,ireg(1)),(parm,iparm(1)) 
C 
C 4.  CONSTANTS USED
C 
C 
C 5.  INITIALIZED VARIABLES 
C 
      data ilen/40/ 
C 
C     PROGRAM STRUCTURE 
C 
C     1. If class buffer contains command name with "=" then we have
C     parameters to set tempwx.  If only the command name is present, 
C     then report tempwx.
      nrec = 0
C 
      iclcm = ip(1) 
      ierr = 0
      ichold = -99
      if (iclcm.eq.0) then
        ierr = -1
        goto 990
      endif
      call ifill_ch(ibuf,1,ilen,' ')
      ireg(2) = get_buf(iclcm,ibuf,-ilen,idum,idum)
      nchar = min0(ireg(2),ilen)
      ieq = iscn_ch(ibuf,1,nchar,'=') 
      if (ieq.eq.0) goto 500
C                   If no parameters, go report tempwx
      if (cjchar(ibuf,ieq+1).eq.'?') then
        ip(4) = o'77'
C       IP(5) = ICLCM
        call fixtmpdis(ip,iclcm)
        return
      endif
C 
C 
C     2. Step through buffer getting each parameter and decoding it.
C     Command from user has these parameters: 
C                   fixtmp=<tempC>
C     The tempC has no default. 
C 
      ich = 1+ieq 
      call gtprm2(ibuf,ich,nchar,2,tempc,ierr)
C                   Pick up temperature, real number
      if(ierr.lt.0) then
         ierr=-201
         goto 990
      else if (ierr.eq.1) then !no old value
         ierr=-301
         goto 990
      else if (ierr.eq.2) then     !   error if default specified
        ierr = -101
        goto 990
      else if (tempc.gt.50.0.or.tempc.lt.-50.0) then
        ierr = -201
        goto 990
      endif
C 

C     4. Now plant these values into COMMON.
C 
      tempwx=tempc
      call fs_set_tempwx(tempwx)
      goto 990
C 
C 
C     5.  This is the report value section.
C 
500   continue
      call fixtmpdis(ip,iclcm)
      return
C
990   ip(1) = 0
      ip(2) = 0
      ip(3) = ierr
      call char2hol('st',ip(4),1,2)
      return
      end
