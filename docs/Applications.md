# Applications

Each application is listed here with the necessary instructions to build it from source.

Note that all tools go into the `/opt/bioit` directory followed by their name and then versions for each. This way we can keep all versions of tools available. By default RPMs are built that set the alternatives for each tool to the latest version so users will always have the best version but they can also use the environment modules to choose another version.

## Notes on installing rstudio

Install the latest Rstudio Server using the following:

    wget https://download2.rstudio.org/server/centos7/x86_64/rstudio-server-rhel-1.4.1717-x86_64.rpm
    sudo yum install rstudio-server-rhel-1.4.1717-x86_64.rpm

Open firewall port to allow this to work:

    sudo firewall-cmd --zone=public --add-port=8787/tcp --permanent
    sudo firewall-cmd --reload

## Notes on installing jupyterlab

Ensure SE Linux is turned off by editing `/etc/selinux/config` and setting `SELINUX=disabled` then reboot the server.

Create a self-signed certificate for the server to use as it runs on port 443. This command will create files for the server.

    sudo mkdir /etc/ssl/private
    sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/ssl/private/`hostname`.key -out /etc/ssl/certs/`hostname`.crt

Answer the questions with sensible values.

Run the `build_jupyterlab` script which will download everything it needs and use the cert you just created.

Once that completes open port 443 on the firewall:

    sudo firewall-cmd --zone=public --add-port=443/tcp --permanent
    sudo firewall-cmd --reload

Users can now go to <https://localhost> and they should see the login prompt.

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
* [gvcftools](gvcftools.md)
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
