'''
Created on 01-06-2012

@author: anna
'''
from django import template

register = template.Library()

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

def rep(value, arg):
    return value.replace(arg,' ')

@register.filter
def insert_spaces(value):
    newValue=''
    for l in value:
        newValue=l+''
    return newValue

@register.filter 
def process_system_part(system_part):
    if '<System>' in system_part:
            system_part='First protein of the genomic cluster of restriction-modification related proteins'
    elif '<middle>' in system_part:
            system_part='Located In the middle the genomic cluster of restriction-modification related proteins'
    elif '</System>' in system_part:
            system_part='Last protein of the genomic cluster of restriction-modification related proteins'
    elif '<Solitary>' in system_part:
            system_part='It is not associated with the genomic cluster of restriction-modification related proteins'
    elif '<not>' in system_part:
            system_part='It is not restriction-modification related protein'
    return system_part
#seting M R S

@register.filter
def process_subunit_kind(subunit_kind):           
    if 'M' in subunit_kind:
            subunit_kind='Methylase'
    elif 'R' in subunit_kind:
            subunit_kind='Restrictase' 
    elif 'S' in subunit_kind:
            subunit_kind='Specificity subunit' 
    return subunit_kind
    #cuting out first letter from gene_id  
    
@register.filter
def process_gene_id(gene_id): 
    gene_id= gene_id.split('.')
    gene_id=gene_id[1]
    return  gene_id
#format HammerCluster
@register.filter
def process_hammer_cluster(hammer_cluster): 
    if hammer_cluster!='':
        hammer_cluster=hammer_cluster.replace('_HMMER','')
    return hammer_cluster

#format aa_sequence

@register.filter
def process_aa_sequence(aa_sequence):
   
    new_aa_sequence=''                    
    for idx, leter in enumerate(aa_sequence):
        if idx%80!=0:
            new_aa_sequence=new_aa_sequence+leter
        else:
            new_aa_sequence=new_aa_sequence+' '+leter
    aa_sequence=new_aa_sequence
    return aa_sequence

#seting DNA piece Name    

@register.filter
def process_dnapiece_name(dnapiece_name):
    dnapiece_name=dnapiece_name.split('.')
    dnapiece_name=dnapiece_name[0]
    return dnapiece_name
@register.filter    
def process_genome_name(genome_name):
    genome_name=genome_name.replace('_',' ')
    return genome_name
@register.filter  
def anias_div(value):
    """gets floor from division by arg if value<-10 or >6"""
    value=int(value)
    result=0
    if value<-30 or value>45:
        result=value//15
    elif value>-30 and value<0:
        result=-3
    elif value>0 and value <45:
        result=2
    return result  

register.filter('cut', cut)
register.filter('lower', lower)
register.filter('rep', rep)