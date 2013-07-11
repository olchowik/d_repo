from django.db import models
    
class Genome(models.Model):
    #genome name
    name = models.CharField(unique=True, max_length=70)
   
    #This is what gets printed when we call this objects
    def __unicode__(self):
        return 'Genome of: ' + self.name
    
class DNAPiece(models.Model):
    #Reference to the genome (Genome-type object) in which the piece of DNS is located.
    genome = models.ForeignKey(Genome)
    #Name of the .ptt file (from the ncbi ftp site) with data on this piece of DNA
    name = models.CharField(unique=True, max_length=70)
   
    def __unicode__(self):
        return ('DNA piece: ' + self.name
        #use self.ForeignKey.attribute to access attribute of the Foreign Key -> here genome
                + ' in: ' + self.genome.name)
        
'''To improve:
 subunit_composition, family_composition, subunit_family_composition, and probebly system_kind
 Could have been created dynamically basing of proteind when object is created.
 **This would simplify new data entry**
 
 Proposed solution/
 1)use __init__ function??
 2)get all the proteins that belong to this system: system.protein_set
 3)create  subunit_composition using system.protein_set.subunit_kind
 and family_composition system.protein_set.subunit_kind.hammer_cluster
 4)subunit_family_composition basing on two previously created fields
 
'''
    
class System(models.Model):
    #reference to a piece of DNA in the cell (DNAPiece-type object) (.ptt file)  on which this system is located
    dnapiece = models.ForeignKey(DNAPiece)
    # e.g. MRS means that there is M, R and S subunit exactly in this order on the DNA
    subunit_composition = models.CharField(max_length=70)
    # G_G_M lists families to which each subunit was classified
    family_composition = models.CharField(max_length=70)
    # e.g. MG_SG_RA means subunit M from family G, subunit S from G, R from family A.
    subunit_family_composition = models.CharField(max_length=140)
    # This is result of our 'inner classification'. If system had 1 M 1R and 1 or more S
    # and all the subunits belonged to the same family it was automatically classified into this family
    system_kind = models.CharField(max_length=10)
    #
    real_name = models.CharField(max_length=20)
   
    def __unicode__(self):
        return ('System number: ' + str(self.id)
                + ' Composed of: ' + self.subunit_composition
                + ' subunits that belong to family ' + self.family_composition
                #it's a bit redundant:
                #+ ' respectively, you can write it as: ' + self.subunit_family_composition
                + '. System classified as: ' + self.system_kind
                #use self.ForeignKey.AnotherForeignKey.attribute
                +' It is in: ' + self.dnapiece.genome.name
                +' on: ' + self.dnapiece.name) 
    
class Protein(models.Model):
    #reference to a system (System-type object) that this protein belongs to
    system = models.ForeignKey(System)
    # e.g. 1234567 ->GI
    gene_id = models.CharField(unique=True, max_length=20)
    # e.g.1456...2345 position on the DNA strand (from .ptt file)
    genome_location = models.CharField(max_length=30)
    # e.g. + -> the DNA strand (plus or minus)
    strand = models.CharField(max_length=5)
    # e.g. 14 number of bp between the gene and previous gene in this system
    # 0 for start of the system
    margin_left = models.IntegerField()
    #<System>->first protein of the system or 2 or more subunits
    #<middle> in the middle of the system
    #</System> last protein of the system
    #<Solitary> -> M R or S but not in any of the systems
    #<not> It is not M , R or S subunit
    system_part = models.CharField(max_length=20)
    #Family as defined by clans (only 'most confident' proteins attributed to clusters)
    clans_cluster = models.CharField(max_length=5) #nie ma w all-tabelce
    #Family as assigned by HMMer
    hammer_cluster = models.CharField(max_length=5)
    # M for methyltransferase
    # R for restrictase
    # S for specificity subunit
    #   for proteins that are not M R or S
    subunit_kind = models.CharField(max_length=5)
    # length of the protein in bp
    dna_length = models.IntegerField()
    #amino acid sequence of this protein
    aa_sequence = models.TextField()
    #result
    hh_pfam_id = models.CharField(max_length=10)
    hh_pfam_short_desc = models.CharField(max_length=40)
    hh_probability = models.DecimalField(max_digits=5, decimal_places=2)
    hh_e_value = models.CharField(max_length=10)
    hh_pfam_desc = models.TextField()
    # Probabilities form Alberta's data
    m_probability = models.IntegerField() #Wilno
    r_probability = models.IntegerField() #Wilno
    s_probability = models.IntegerField() #Wilno
    
    def __unicode__(self):
        s_kind = ', subunit kind: '
        if self.subunit_kind == '':
            s_kind = ''
        return ('Gene id: ' + self.gene_id + ', located on ' + self.system.dnapiece.name
                + ' in ' + self.system.dnapiece.genome.name + ', system part: '
                + self.system_part + s_kind + self.subunit_kind + ' ' + self.hh_pfam_short_desc)
    