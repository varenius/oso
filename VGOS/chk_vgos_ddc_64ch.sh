#!/bin/bash
prt_help()
{
	echo "NAME"
	echo "    chk_vgos_ddc_64ch.sh -- report sampler statistical distribution and plot bandpass"
	echo "SYNOSIS"
	echo "    chk_vgos_ddc_64ch.sh data_format data_file out_dir"
	echo "INPUT"
	echo "    data_format: the string reported by mk5c_mode/bit_stream. e.g. VDIF_8000-2048-16-2"
	echo "    data_file: input VDIF file to process"
	echo "    out_dir: where to store output"
	echo "OUTPUT"
	echo "    Using the specified out_dir:"
	echo "    (1) Sampler statistical distribution: m5bstate.txt"
	echo "    (2) Auto-correlation spectrum data:m5spec.txt"
	echo "    (3) Bandpass plots: bandpass.ps"
}

if [[ -z ${1} ]]  
then 
	echo "ERROR 1: Please input the data format. "
	echo ""; prt_help ; exit 11
else
	data_format=${1}
fi

if [[ -z ${2} ]]  
then 
	echo "ERROR 2: Please input data_file."
	echo ""; prt_help ; exit 11
else
	data_file=${2}
fi

if [[ -z ${3} ]]  
then 
	echo "ERROR 3: Please input out_dir."
	echo ""; prt_help ; exit 11
else
	out_dir=${3}
fi

#n_frame=40000
n_frame=10000
#np_per_mhz=1024    #number of FFT points per MHz, i.e. frequency resolution
#np_per_mhz=512    #number of FFT points per MHz, i.e. frequency resolution
#np_per_mhz=256    #number of FFT points per MHz, i.e. frequency resolution
np_per_mhz=128    #number of FFT points per MHz, i.e. frequency resolution
#np_per_mhz=64    #number of FFT points per MHz, i.e. frequency resolution

temp_string="${data_format}"
array_mode=(${temp_string//-/ })
n_mbps=${array_mode[1]}
n_subband=${array_mode[2]}
n_bit=${array_mode[3]}
bbc_mhz=` echo " ${n_mbps} / ${n_subband} / ${n_bit} / 2 " | bc `
if [[ -z ${bbc_mhz} ]] ; then echo "BBC bandwith is not defined." && exit 11 ; fi
fft_chan=` echo "${np_per_mhz} * ${bbc_mhz}" | bc `
if [[ -z ${fft_chan} ]] ; then echo "Number of FFT points is not defined." && exit 11; fi
echo "BBC bandwidth is ${bbc_mhz} and Number of FFT points: ${fft_chan}"
out_m5bstate="${out_dir}/m5bstate.txt"
out_m5spec="${out_dir}/m5spec.txt"
out_bandpass="${out_dir}/bandpass.ps"
zoom_in=7    #Zoomed in by a factor in the middel panel 
zoom_pos=0.5 # the relative position willing to zoom in. Central position: 0.5 
data_time=`m5time ${data_file} ${data_format} |grep MJD`  
if [[ -z ${data_time} ]]
then
    echo "ERROR 3: Problem with running m5time ${data_file} ${data_format}"
	echo ""; exit 13
fi
array_date=(${data_time//\// })
data_mjd=${array_date[2]}
unix_time=` echo "(${data_mjd} - 40587) * 86400" | bc `
plot_date=` date --date="@${unix_time}" "+%Y %b %d" `
plot_hms=${array_date[3]}
plot_time="${plot_date}  ${plot_hms:0:8}"

data_date=` date --date="@${unix_time}" +%Yy%mm%dd `
data_hms=${plot_hms/:/h} 
data_hms=${data_hms/:/m}
data_hms=${data_hms:0:8}
data_time="${data_date}${data_hms}s"

out_m5bstate="${out_dir}/m5bstate_${data_time}.txt"
data_m5bstate="${out_dir}/m5bstate_data.txt"
out_m5spec="${out_dir}/m5spec_${data_time}.txt"
out_bandpass="${out_dir}/bandpass_${data_time}.ps"
/usr/local/difx-trunk/bin/m5bstate ${data_file} ${data_format} ${n_frame} > ${out_m5bstate} 
/usr/local/difx-trunk/bin/m5spec -dbbc -nopol ${data_file} ${data_format} ${fft_chan} ${n_frame} ${out_m5spec} >> /dev/null  

if ! [[ -f ${out_m5spec} ]]
then
    echo "ERROR 4: Missing the file of ${out_m5spec}"
	echo ""; exit 14
fi
awk "NR>=19" ${out_m5bstate} > ${data_m5bstate}
gnuplot <<-EOF_PLOT
   set term postscript landscape enhanced color solid
   set output "${out_bandpass}"
   set multiplot layout 1,3 title "Data Beginning UT: ${plot_time}"
   plot_data="${out_m5spec}"
   set tmargin 0.5
   set rmargin 1
   set tics scale 1.8
   

# - - - - - - - - - - - - - - - - - - - - -
# - plot bandpass of the first 32 channels
# - - - - - - - - - - - - - - - - - - - - -

   set xlabel "Frequency (MHz, ${np_per_mhz} pts/MHz)"
#  set ylabel "Log10 auto-correlation amplitude shifted by adding channel number" offset 1.5,0
   set xrange [-0.5:${bbc_mhz}+0.5]
   set ytics 8
   set mytics 5
   set mxtics 5 
#  set yrange[0:${n_subband}+2]
   set yrange[0:34]
   set label "if-a" at -5,4
   set label "if-b" at -5,12
   set label "if-c" at -5,20
   set label "if-d" at -5,28
#  plot  for [col=2:(${n_subband}+1)] plot_data using 1:(log10(column(col)) + col - 1) with lines title ''
#   plot  for [col=2:(${n_subband}+1)] plot_data using 1:((column(col)) + col - 1) with lines title ''
   plot  for [col=2:9] plot_data using 1:(log10(column(col)) + col - 1)   with lines title '' lt rgb "black", \
         for [col=10:17] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "red", \
         for [col=18:25] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "black", \
         for [col=26:33] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "red"

# - - - - - - - - - - - - - - - - - - - - -
# - plot bandpass of the second 32 channels
# - - - - - - - - - - - - - - - - - - - - -

   unset label
   set xlabel "Frequency (MHz, ${np_per_mhz} pts/MHz)"
#  set ylabel "Log10 auto-correlation amplitude shifted by adding channel number" offset 1.5,0
   set xrange [-0.5:${bbc_mhz}+0.5]
   set ytics 8
   set mytics 5
   set mxtics 5 
#  set yrange[0:${n_subband}+2]
   set yrange[31:66]
   set label "if-e" at -5,36
   set label "if-f" at -5,44
   set label "if-g" at -5,52
   set label "if-h" at -5,60
   plot  for [col=34:41] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "black", \
         for [col=42:49] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "red", \
         for [col=50:57] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "black", \
         for [col=58:65] plot_data using 1:(log10(column(col)) + col - 1) with lines title '' lt rgb "red"


# - - - - - - - - - - - - - - - - - - - - - - - -
# - plot sampler statistics for all 64 channels
# - - - - - - - - - - - - - - - - - - - - - - - -

   unset label
   set rmargin 1
   plot_data="${data_m5bstate}"
   set xlabel "Percentage of samplers"
   set ylabel "Channel number" offset 1.5,0
   set xrange [*:*]
   set yrange[0:${n_subband}+2]
   set xtics 5
   set ytics 2
   set mxtics 5
   set mytics 1
   set label "if-a" at 35,4
   set label "if-b" at 35,12
   set label "if-c" at 35,20
   set label "if-d" at 35,28
   set label "if-e" at 35,36
   set label "if-f" at 35,44
   set label "if-g" at 35,52
   set label "if-h" at 35,60
   unset grid
   set key center top horizontal box spacing 0.75
   nn_bit=${n_bit}
   
   if ( nn_bit == 2 ) plot \
         plot_data using (column(9)):(column(1)+1)  title '{/Symbol +} {/Symbol +}', \
         plot_data using (column(6)):(column(1)+1)  title '{/Symbol -} {/Symbol -}',\
         plot_data using (column(8)):(column(1)+1)  title '{/Symbol +}', \
         plot_data using (column(7)):(column(1)+1)  title '{/Symbol -}', \
		 plot_data using (26):(column(1)+1):(sprintf("g=%3.2f", column(10))) with labels notitle  
   if ( nn_bit == 1 ) plot \
        plot_data using (column(5)):(column(1)+1)  title '{/Symbol +}', \
        plot_data using (column(4)):(column(1)+1)  title '{/Symbol -}'
   unset multiplot
EOF_PLOT

link_m5bstate="${out_dir}/m5bstate.txt"
link_m5spec="${out_dir}/m5spec.txt"
link_bandpass="${out_dir}/bandpass.ps"

ln -sf ${out_m5bstate} ${link_m5bstate}
ln -sf ${out_m5spec}   ${link_m5spec}
ln -sf ${out_bandpass} ${link_bandpass}


