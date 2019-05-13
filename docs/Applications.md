# Applications

Each application is listed here with the necessary instructions to build it from source.

Note that all tools go into the `/opt/bioit` directory followed by their name and then versions for each. This way we can keep all versions of tools available. By default RPMs are built that set the alternatives for each tool to the latest version so users will always have the best version but they can also use the environment modules to choose another version.

## Notes on installing rstudio

The latest rstudio 1.2 requires `libxkbcommon-x11` to be installed. Also, the first time a user starts rstudio, they'll need to run the following:

    QMLSCENE_DEVICE=softwarecontext rstudio

This will set the rendering engine to software mode required to start under X2Go. Once they're in, they go go into the options and set software rendering to be the default and then they'll be able to start it from the menu.

## List of applications and instructions on building them

* [abyss](abyss.md)
* [augustus](augustus.md)
* [bamtools](bamtools.md)
* [bbmap](bbmap.md)
* [bcftools](bcftools.md)
* [bedtools2](bedtools2.md)
* [bismark](bismark.md)
* [bowtie](bowtie.md)
* [bowtie2](bowtie2.md)
* [bwa](bwa.md)
* [cutadapt](cutadapt.md)
* [ea-utils](ea-utils.md)
* [FastQC](FastQC.md)
* [hisat2](hisat2.md)
* [hmmer](hmmer.md)
* [htslib](htslib.md)
* [igv](igv.md)
* [ncbi-blast](ncbi-blast.md)
* [nxtrim](nxtrim.md)
* [picard](picard.md)
* [R-core](R-core.md)
* [rtg-tools](rtg-tools.md)
* [samtools](samtools.md)
* [SOAPdenovo2](SOAPdenovo2.md)
* [SolexaQA++](SolexaQA.md)
* [stringtie](stringtie.md)
* [tophat](tophat.md)
* [vcftools](vcftools.md)
* [velvet](velvet.md)
* [vsearch](vsearch.md)
