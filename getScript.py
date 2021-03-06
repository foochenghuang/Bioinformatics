#! /usr/bin/python3
import argparse,os,shutil
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
-------------------
Simple Introduction:
Generate the assembly script for each sample.
Example: python3 diversity.py -i GeneCatalog_profile.xls.gz
To be continued.
------------------'''
)
parser.add_argument('-i','--Input', help = "the RemoveHost_Data.list file.")
parser.add_argument('-s','--tool', help = "megahit (default) or metaspades.")
#parser.add_argument('-p','--process', help = "the directory for results.")
parser.add_argument('-o','--outdir',help = "the output directory, full path.")
#parser.add_argument('-o','--outdir',help = "the output directory,default is current working directory.",nargs='?')
parser.add_argument("-v", "--version",action='version', version='%(prog)s 1.0')
args = parser.parse_args()
(removeHostList,tool,outdir) = (args.Input,args.tool,args.outdir)
par = [removeHostList,tool,outdir]

if not all(par):
	parser.print_help()
	exit()

if os.path.exists(outdir):
#	os.removedirs(outdir)
	shutil.rmtree(outdir)

os.makedirs(outdir)	
shelldir = outdir + '/shell'
processdir = outdir + '/process'
os.makedirs(shelldir)
os.makedirs(processdir)

with open(removeHostList,'r') as IN:
	for line in IN:
		lst = line.strip('\n').split('\t')
		(ID,rmfq1,rmfq2) = (lst[0],lst[1],lst[2])
		shellIDdir = shelldir + '/' + ID
		os.makedirs(shellIDdir)
		shellfile_path = shellIDdir + '/' + ID + '_assembly.sh'
		processIDdir = processdir + '/' + ID 
		os.makedirs(processIDdir) # make sample dir
		gunzip_rmfq1_path = processIDdir +'/' + ID + '.RemoveHost_1.fastq'
		gunzip_rmfq2_path = processIDdir +'/' + ID + '.RemoveHost_2.fastq'
		metawrap_path = '/ifswh1/BC_PUB/biosoft/BC_NQ/01.Soft/03.Soft_ALL/metaWRAP-181018/bin/metawrap'
		out = open(shellfile_path,'w') 
		print('export PATH=/ifswh1/BC_PS/wangpeng7/Software/metaWRAP-181018/bin:$PATH', file=out)
		print('export PATH=/ifswh1/BC_PS/wangpeng7/Software/metaSPAdes/SPAdes-3.13.0-Linux/bin:$PATH', file=out)
		print('export PATH=/ifswh1/BC_PUB/biosoft/BC_NQ/01.Soft/03.Soft_ALL/Python-2.7.5/Built/bin:$PATH', file=out) # for quast
		print('export PATH=/ifswh1/BC_PUB/biosoft/pipeline/MICRO/Meta/Meta_Metagenomic_Survey_2017a/modules/Assembly/Assembly_megahit/bin/megahit:$PATH', file=out)
		print('gunzip -c ' + rmfq1 + ' > ' + gunzip_rmfq1_path, file=out)
		print('gunzip -c ' + rmfq2 + ' > ' +  gunzip_rmfq2_path, file=out)
		if tool == 'metaspades':
			print(metawrap_path + ' assembly -1 ' + gunzip_rmfq1_path + ' -2 ' + gunzip_rmfq2_path + ' -m 100 -t 20 --metaspades -o ' + processIDdir, file=out)  # later change the par
		else:
			print(metawrap_path + ' assembly -1 ' + gunzip_rmfq1_path + ' -2 ' + gunzip_rmfq2_path + ' -m 100 -t 20 --megahit -o ' + processIDdir, file=out)
		print('rm ' + gunzip_rmfq1_path, file=out)
        	print('rm ' + gunzip_rmfq2_path, file=out)
