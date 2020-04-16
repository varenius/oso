      subroutine wx(ip,itask)
C 
C     Local WX
C     for Onsala,  M. Lindqvist and R. Haas - November 2005
C 
C     INPUT VARIABLES:
C 
      dimension ip(5) 
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
      integer*2 ibuf2(40), ibuf(20)
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
      real*8 JD, tp, pr, rh, ws, wd
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
crh   iclcm = ip(1) 
crh   ierr = 0
crh   ichold = -99
crh   if (iclcm.eq.0) then
crh     ierr = -1
crh     goto 990
crh   endif
crh   call ifill_ch(ibuf,1,ilen,' ')
crh   ireg(2) = get_buf(iclcm,ibuf,-ilen,idum,idum)
crh   nchar = min0(ireg(2),ilen)
crh   ieq = iscn_ch(ibuf,1,nchar,'=') 
crh   if (ieq.eq.0) goto 500
C                   If no parameters, go report tempwx
      if (cjchar(ibuf,ieq+1).eq.'?') then
        ip(4) = o'77'
C       IP(5) = ICLCM
CC        call fixtmpdis(ip,iclcm)
        return
      endif
C 
C 
C     2. Step through buffer getting each parameter and decoding it.
C     Command from user has these parameters: 
C                   fixtmp=<tempC>
C     The tempC has no default. 
C 
CC      ich = 1+ieq 
CC      call gtprm2(ibuf,ich,nchar,2,tempc,ierr)
C                   Pick up temperature, real number
CC      if(ierr.lt.0) then
CC         ierr=-201
CC         goto 990
CC      else if (ierr.eq.1) then !no old value
CC         ierr=-301
CC         goto 990
CC      else if (ierr.eq.2) then     !   error if default specified
CC        ierr = -101
CC        goto 990
CC      else if (tempc.gt.50.0.or.tempc.lt.-50.0) then
CC        ierr = -201
CC        goto 990
CC      endif
C 
      tp=-999
      pr=-999
      rh=-999
      ws=-999
      wd=-999
      call weather(JD, tp, pr, rh, ws, wd)
crh   write(*,*)tp,pr,rh,ws,wd

C     4. Now plant these values into COMMON.
C 
      tempwx  = tp
      preswx  = pr
      humiwx  = rh
      speedwx = ws
      direcwx = wd

      call fs_set_tempwx(tempwx)
      call fs_set_preswx(preswx)
      call fs_set_humiwx(humiwx)
CC      goto 990
C 
C 
C     5.  This is the report value section.
C 
 500  continue
CC      call fixtmpdis(ip,iclcm)
crh   return
C
C
C     5. Finally, code up the message for BOSS and the display and log.
C
      nch = ichmv_ch(ibuf2,nchar+1,'wx/')
crh "wx" explicitely added in string - rh 2005.11.11
      if (tempwx.GE.-50.0) then
         nch = nch + ir2as(tempwx,ibuf2,nch,5,1)
      endif
      if (speedwx.GE.0.0.OR.humiwx.GE.0.0.OR.preswx.GE.0.0) then
         nch = mcoma(ibuf2,nch)
      endif
      if (preswx.GE.0.0) then
         nch = nch + ir2as(preswx,ibuf2,nch,7,1)
      endif
crh   if (preswx.GE.0.0) then
crh      nch = nch + ir2as(preswx,ibuf2,nch,7,1)
crh   endif
      if (speedwx.GE.0.0.OR.humiwx.GE.0.0) then
         nch = mcoma(ibuf2,nch)
      endif
      if (humiwx.GE.0.0) then
         nch = nch + ir2as(humiwx,ibuf2,nch,5,1)
      endif
crh - - - - - - - - - - - - - - - - - -
crh  log also wind speed and direction
crh - - - - - - - - - - - - - - - - - -
      if (speedwx.GE.0.0.OR.direcwx.GE.0.0) then
         nch = mcoma(ibuf2,nch)
      endif
      if (speedwx.GE.0.0) then
         nch = nch + ir2as(speedwx,ibuf2,nch,5,1)
      endif
      if (direcwx.GE.0.0) then
         nch = mcoma(ibuf2,nch)
      endif
      if (direcwx.GE.0.0) then
         nch = nch + ir2as(direcwx,ibuf2,nch,7,1)
      endif
crh - - - - - - - - - - - - - - - - - -
crh
crh - - - - - - - - - - - - - - - - - -
C      if(MET3.eq.wx_met) then
crh   if (speedwx.GE.0.0.OR.humiwx.GE.0.0) then
crh      nch = mcoma(ibuf2,nch)
crh   endif
crh   if (humiwx.GE.0.0) then
crh      nch = nch + ir2as(humiwx,ibuf2,nch,5,1)
crh   endif
C      if(MET3.eq.wx_met) then
C         if (speedwx.GE.0.0) then
C            nch = mcoma(ibuf2,nch)
C            nch = nch + ir2as(speedwx,ibuf2,nch,7,1)
C            nch = mcoma(ibuf2,nch)
C            nch = nch + ib2as(directionwx,ibuf2,nch,o'100000'+3)
C         endif
C      endif
C
      iclass = 0
      nch = nch - 1
      call put_buf(iclass,ibuf2,-nch,'fs','  ')

      ip(1)=iclass
      ip(2)=1
      ip(3)=0   
      return

990   ip(1)=0
      ip(2)=0
      ip(3)=ierr   
      call char2hol('st',ip(4),1,2)
      return
      end
