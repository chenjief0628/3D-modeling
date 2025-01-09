


################################################################################
 ___    _____  _    ____ ____  _____ ____       ____  _   _    _    
|_ _|  |_   _|/ \  / ___/ ___|| ____|  _ \     |  _ \| \ | |  / \   
 | |_____| | / _ \ \___ \___ \|  _| | |_) |____| |_) |  \| | / _ \  
 | |_____| |/ ___ \ ___) |__) | |___|  _ <_____|  _ <| |\  |/ ___ \ 
|___|    |_/_/   \_\____/____/|_____|_| \_\    |_| \_\_| \_/_/   \_\

I-TASSER-RNA is a program for accurate de novo RNA tertiary structure prediction

Note, this is the stand-alone program, users mya also submit jobs to
https//zhanggroup.org/I-TASSER-RNA
######################### INSTALLATION INSTRUCTIONS ############################

System requirements: x86_64 machine, Linux kernel OS, Free disk space of more 
	than 500GB. The vast majority of the disk space will be used to store the 
	sequence databases.
 
######################## General information on how to run I-TASSER-RNA ############
a, RNA 3D modeling needs 
   1. RNA sequence-structure local threading meta-alignment
      algorithm for full-length initial models and spatial constraints
   2. inter-nucleotide distance prediction by a deep residual network 
   3. submit RNA3D simulation jobs for first-round simulation
   4. cluster decoys and refine cluster centroid models for second-round simulation
   5. final model selection and all-atom model construction
      
 ######################## Each program in I-TASSER-RNA #################################
 
a, collect all templates by threading program and other predition programs
1. input features
   seq.fasta (query fasta)
2. output
   seq.afa (MSA from rMSA)
   seq.a2m_msa (MSA from RNAcamp3)
   seq.a2m (MSA from RNAcentral by Infernal)
   template/*pdb
   
b, inter-nucleotide geometires prediction
   1. input features 
      seq.fasta (query fasta)
      seq.afa (MSA from rMSA)
      seq.a2m_msa (MSA from RNAcamp3)
      seq.a2m (MSA from RNAcentral by Infernal)
   2. output
      npz_dist_p.txt  (distance between p-p)
      npz_dist_c4.txt  (distance between c4'-c4')
      npz_dist_n.txt  (distance between n-n)
      npz_angle_theta.txt  (angles <p-c4-p-c4> and <c4-p-c4-p>)

c, folding simulation
   1. input files
      *_model.pdb (initial full-length  models built by threading templates)
      contactnn.dat (dNiNj<10 in two nucleotides with |i-j|>9nt;i j P N top40)
      contactpp.dat (dPiPj<20 in two nucleotides with |i-j|>9nt;i j P N top40)
      distL_8L.dat (i+j*8;i=1,2...L;J=2;top3)
      distL_10L.dat (i+j*10;top3)
      short_6L.dat (|i-j|<7;hard top40; easy top 10)
      npz_dist_p.txt  (distance between p-p)
      npz_dist_c4.txt  (distance between c4'-c4')
      npz_dist_n.txt  (distance between n-n)
      npz_angle_theta.txt  (angles <p-c4-p-c4> and <c4-p-c4-p>)
   2. output 
      *conf.dat
      *U.dat
      *uN.dat	

d, optimize simulation
   1. input files
      combo*.dat (cluter centroids as initial models)
   2. output
      CG.dat

e, clustering
   1. input files
      trmsinp   (length of query)
      tseq.dat  (secondary structure information generated by SPOT_RNA)
      ttra.in   (prepare decoys for clustering)
   2. output
      combo.dat (cluster centeriod for each cluster)
      close1.dat (cluster center)

f, all-atom model construction
   1. input files
      frag_.dat (fragment of A,U,C,G by all atom)
      CG.dat  (coarse-grained model from simulation)


##############################install the third party programs ################

Note, users are responsible for adhering to the licenses for these programs, 
which include:
		AF3, DRfold2, DeepFoldRNA, RoseTTAFoldNA, RhoFold, 
		trRosettaRNA,SimRNA: used for tertiary structure prediction
  		( https://github.com/robpearc/DeepFoldRNA
		  https://yanglab.qd.sdu.edu.cn/trRosettaRNA/download/
		  https://github.com/leeyang/DRfold/	
    	          https://github.com/ml4bio/RhoFold
	          https://github.com/uw-ipd/RoseTTAFold2NA
                  https://ftp.users.genesilico.pl/software/simrna/version_3.20/SimRNA_64bitIntel_Linux.tgz
		)
  		
		PETfold: used for secondary structure prediction 
		(https://rth.dk/resources/petfold/)
		This program was developed Rolf Backofen's and Søren Brun's Lab
		Citation: Seemann SE, Gorodkin J, Backofen R. Nucleic Acids Res., 
			36(20):6355-62, 2008

		rMSA: used for MSA generation (https://github.com/pylelab/rMSA)
		This program was developed by Chengxin Zhang at Anna Pyle's Lab	
                Citation: Zhang C, Zhang Y, Pyle AM (2021) rMSA: accurate multiple 
			sequence alignment generation to improve RNA structure modeling. 
			ISMB, webinar.

