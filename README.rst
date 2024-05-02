
================
QconCATquantSTAR
================

Description
===========

The ``QconCATquantSTAR.py`` script allows the quantification of endogenous proteins for which a QconCAT internal standard was spiked-in. Protein abundances from a DDA method analysed with ProteomeDiscoverer (Thermo Fisher Scientitific, Waltham, MA, USA) are used for protein quantification in combination with concentration values of spiked-in QconCAT standard proteins.

The repository is supporting material for the `STAR protocol <https://doi.org/10.1016/j.xpro.2023.102060>`_ "Protocol for absolute quantification of proteins in Gram-negative bacteria based on QconCAT-based labeled peptides".

Input data
==========

The DDA PeptideGroups results table (.CSV file) should be exported from ProteomeDiscoverer. This results table should at least include the following headers: ``Annotated Sequence``, ``Modifications``, ``Master Protein Accessions``, and ``Abundances (Normalized): F{X}: Sample`` for each sample X. An example DDA PeptideGroups results table is located in the ``Examples`` folder as ``DDA_PeptideGroups_example.csv``.

The QconCAT input table (.CSV file) should have the following structure including headers. The ``FullPeptideName`` column should have the sequence of each peptide included in the QconCAT internal standards, the ``ProteinName`` column should have the UniProt identifier of the endogenous protein of the corresponding peptide sequence, and the ``Concentration`` column should have the spiked-in concentration of each QconCAT peptide. An appropriate concentration unit would be fmol/µg total protein, since the spiked-in QconCAT protein and the corresponding QconCAT peptides have equimolar concentration. The unit of concentration used in the QconCAT input table will be the unit of concentration in the output table with the quantified endogenous proteins.

================ ============= ================
FullPeptideName  ProteinName   Concentration
================ ============= ================
sequence 1       UniProt ID 1  concentration 1
sequence 2       UniProt ID 2  concentration 2
...              ...           ...
sequence N       UniProt ID N  concentration N
================ ============= ================

An example QconCAT input table is located in the ``Examples`` folder as ``QconCATinfo_example.csv``.

Usage
=====

The ``QconCATquantSTAR.py`` script can be used as follows:

::

    python QconCATquantSTAR.py -i ./Examples/DDA_PeptideGroups_example.csv -Q ./Examples/QconCATinfo_example.csv
    
The DDA PeptideGroups results table and the QconCAT input table should be given as the ``i`` and the ``Q`` argument, respectively.

The output will be generated at ``QconCATproteins.csv``. The output table is formatted with the following column headers: ``ProteinName`` (UniProt identifier of the quantified endogenous protein) and ``conc_sample{X}`` (concentration of the quantified endogenous protein). There will be as many columns with concentrations as there are samples. An example output table is located in the ``Examples`` folder as ``QconCATproteins_example.csv``.
