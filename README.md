<div align="center">
   
  <h1>HiIP 🔬</h1>
  
  **_long pipeline name_**

  [![tests](https://github.com/OpenOmics/HiIP/workflows/tests/badge.svg)](https://github.com/OpenOmics/HiIP/actions/workflows/main.yaml) [![docs](https://github.com/OpenOmics/HiIP/workflows/docs/badge.svg)](https://github.com/OpenOmics/HiIP/actions/workflows/docs.yml) [![GitHub issues](https://img.shields.io/github/issues/OpenOmics/HiIP?color=brightgreen)](https://github.com/OpenOmics/HiIP/issues)  [![GitHub license](https://img.shields.io/github/license/OpenOmics/HiIP)](https://github.com/OpenOmics/HiIP/blob/main/LICENSE) 
  
  <i>
    This is the home of the pipeline, HiIP. Its long-term goals: to accurately ...insert goal, to infer ...insert goal, and to boldly ...insert goal like no pipeline before!
  </i>
</div>

## Overview
Welcome to HiIP! Before getting started, we highly recommend reading through [HiIP's documentation](https://openomics.github.io/HiIP/).

The **`./HiIP`** pipeline is composed several inter-related sub commands to setup and run the pipeline across different systems. Each of the available sub commands perform different functions: 

 * [<code>HiIP <b>run</b></code>](https://openomics.github.io/HiIP/usage/run/): Run the HiIP pipeline with your input files.
 * [<code>HiIP <b>unlock</b></code>](https://openomics.github.io/HiIP/usage/unlock/): Unlocks a previous runs output directory.
 * [<code>HiIP <b>install</b></code>](https://openomics.github.io/HiIP/usage/install/): Download reference files locally.
 * [<code>HiIP <b>cache</b></code>](https://openomics.github.io/HiIP/usage/cache/): Cache remote resources locally, coming soon!

**HiIP** is a comprehensive ...insert long description. It relies on technologies like [Singularity<sup>1</sup>](https://singularity.lbl.gov/) to maintain the highest-level of reproducibility. The pipeline consists of a series of data processing and quality-control steps orchestrated by [Snakemake<sup>2</sup>](https://snakemake.readthedocs.io/en/stable/), a flexible and scalable workflow management system, to submit jobs to a cluster.

The pipeline is compatible with data generated from Illumina short-read sequencing technologies. As input, it accepts a set of FastQ files and can be run locally on a compute instance or on-premise using a cluster. A user can define the method or mode of execution. The pipeline can submit jobs to a cluster using a job scheduler like SLURM (more coming soon!). A hybrid approach ensures the pipeline is accessible to all users.

Before getting started, we highly recommend reading through the [usage](https://openomics.github.io/HiIP/usage/run/) section of each available sub command.

For more information about issues or trouble-shooting a problem, please checkout our [FAQ](https://openomics.github.io/HiIP/faq/questions/) prior to [opening an issue on Github](https://github.com/OpenOmics/HiIP/issues).

## Dependencies
**Requires:** `singularity>=3.5`  `snakemake>=6.0`

At the current moment, the pipeline uses a mixture of enviroment modules and docker images; however, this will be changing soon! In the very near future, the pipeline will only use docker images. With that being said, [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) and [singularity](https://singularity.lbl.gov/all-releases) must be installed on the target system. Snakemake orchestrates the execution of each step in the pipeline. To guarantee the highest level of reproducibility, each step of the pipeline will rely on versioned images from [DockerHub](https://hub.docker.com/orgs/nciccbr/repositories). Snakemake uses singularity to pull these images onto the local filesystem prior to job execution, and as so, snakemake and singularity will be the only two dependencies in the future.

## Installation
Please clone this repository to your local filesystem using the following command:
```bash
# Clone Repository from Github
git clone https://github.com/OpenOmics/HiIP.git
# Change your working directory
cd HiIP/
# Add dependencies to $PATH
# Biowulf users should run
module load snakemake singularity
# Get usage information
./HiIP -h
```

## Contribute 
This site is a living document, created for and by members like you. HiIP is maintained by the members of OpenOmics and is improved by continous feedback! We encourage you to contribute new content and make improvements to existing content via pull request to our [GitHub repository](https://github.com/OpenOmics/HiIP).


## Cite

If you use this software, please cite it as below:  

<details>
  <summary><b><i>@BibText</i></b></summary>
 
```text
Citation coming soon!
```

</details>

<details>
  <summary><b><i>@APA</i></b></summary>

```text
Citation coming soon!
```

</details>


## References
<sup>**1.**  Kurtzer GM, Sochat V, Bauer MW (2017). Singularity: Scientific containers for mobility of compute. PLoS ONE 12(5): e0177459.</sup>  
<sup>**2.**  Koster, J. and S. Rahmann (2018). "Snakemake-a scalable bioinformatics workflow engine." Bioinformatics 34(20): 3600.</sup>  
