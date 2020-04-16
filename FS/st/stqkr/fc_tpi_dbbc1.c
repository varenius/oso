void fc_tpi_dbbc1__(ip,itpis_dbbc)
long ip[5];
int itpis_dbbc[34];
{
    void tpi_dbbc1();

    tpi_dbbc1(ip,itpis_dbbc);

    return;
}
    
void fc_tpput_dbbc1__(ip,itpis_dbbc,isub,ibuf,nch,ilen)
long ip[5];
int itpis_dbbc[34];
int *isub;
char *ibuf;
int *nch;
int *ilen;
{
    void tpput_dbbc1();

    tpput_dbbc1(ip,itpis_dbbc,*isub,ibuf,nch,*ilen);

    return;
}

void fc_tsys_dbbc1__(ip,itpis_dbbc,ibuf,nch,itask,tempwx)
long ip[5];
int itpis_dbbc[34];
char *ibuf;
int *nch;
int *itask;
float *tempwx;
{
    void tsys_dbbc1();

    tsys_dbbc1(ip,itpis_dbbc,ibuf,nch,*itask,*tempwx);

    return;
}
