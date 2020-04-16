void get_tcal_fwhm();

void fc_get_tcal_fwhm1__(device,tcal,fwhm,epoch,flux,corr,ssize,ierr,
			load,sky,tempwx,zero)
char device[2];
float *tcal,*fwhm, *epoch, *flux, *corr, *ssize,*load,*sky,*tempwx,*zero;
int *ierr;
{
get_tcal_fwhm1(device,tcal,fwhm,*epoch,flux,corr,ssize,ierr,
  *load,*sky,*tempwx,*zero);

}
