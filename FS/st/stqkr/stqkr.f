      program stqkr
C
C FORTRAN version of stqkr main
C
C     INPUT VARIABLES:
C         IP(1) - class number containing invocation line
C         IP(2) - branch number, encoded
C
C     OUTPUT VARIABLES:
C         IP(1) - class number, if any
C         IP(2) - number of records in class
C         IP(3) - IERR error code return
C         IP(4) - who caused the error
C
C     COMMON BLOCKS USED
      include '../../fs/include/fscom.i'
C
C 3.  LOCAL VARIABLES
      integer*4 ip(5)                     !  rmpar variables
      integer idum,fc_rte_prior
C
C 6.  HISTORY:
C  WHO  WHEN    DESCRIPTION
C  weh  930807  created sample
C
C     PROGRAM STRUCTURE :
C
C  Get RMPAR parameters, then call the subroutine whose number is in IP(2).
C
      call setup_fscom
      call read_fscom
      idum=fc_rte_prior(FS_PRIOR)
C
C  main loop
C
1     continue
      call wait_prog('stqkr',ip)
      call read_quikr
      isub = ip(2)/100
      itask = ip(2) - 100*isub
C
c three examples:
c
      if (isub.eq.1) then
         call tsys(ip,itask)
      else if (isub.eq.2) then
         call fixtmp(ip,itask)
      else if (isub.eq.3) then
         call wx(ip,itask)
      endif
c
      call write_quikr
      goto 1
      end
