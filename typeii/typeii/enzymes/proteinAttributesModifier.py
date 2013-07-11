'''
Created on 21-05-2012

@author: anna
'''
import collections
from models import Genome, DNAPiece, System, Protein, ProteinForm 
import re
import operator
''''
>TO do : ALL sort dict by values
->Sub comp as bar chart
->Families DH ad 100% vhart
overlap detailed graphs(as%??)
'''
#Modifies this unique protein object
#setting us <System></System> tags to human-readable form 
def numeric_compare(x, y):
    return x - y
def string_to_json(adict, l1,l2, sort_by_key, sort_by_value):
    c_scale=["#FF0F00","#FF6600","#FF9E01","#FCD202","#F8FF01","#B0DE09","#04D215","#0D8ECF","#0D52D1","#2A0CD0","#8A0CCF","#CD0D74"]
    
    if sort_by_value: 
        odict = collections.OrderedDict(sorted(adict.items()))
        adict=odict
        print odict
    if sort_by_key: 
        odict = collections.OrderedDict(sorted(adict.iteritems(), key=operator.itemgetter(1)))
        adict=odict
        print odict
    final_str='['
    counter=0
    for e in adict:
       final_str+='{ '+l1+': "'+str(e)+ '", '+l2+': '+str(adict[e])+', color: "'+c_scale[counter%11]+'" },'
       counter+=1
    final_str=final_str.rstrip(',')
    final_str+=']'
    return final_str
def string_to_100_json(adict, l1,l2,sort_by_key):
    c_scale=["#FF0F00","#FF6600","#FF9E01","#FCD202","#F8FF01","#B0DE09","#04D215","#0D8ECF","#0D52D1","#2A0CD0","#8A0CCF","#CD0D74"]
    key_set=adict.keys()
    if sort_by_key: key_set=sorted( key_set, cmp=numeric_compare)
    print 'value_sorted', key_set
    final_str='['
    counter=0
    for e in adict:
       final_str+='{ '+l1+': "'+str(e)+ '", '+l2+': '+str(adict[e])+', color: "'+c_scale[counter%11]+'" },'
       counter+=1
    final_str=final_str.rstrip(',')
    final_str+=']'
    return final_str
    
def solitary_subunis():
    system_list=System.objects.all()
    adict={}
    for e in system_list:
        subunit_composition=e.subunit_composition
        if len(subunit_composition)<3:
            if subunit_composition not in adict:adict[subunit_composition]=1
            else:adict[subunit_composition]=adict[subunit_composition]+1
    #print 'system_list', adict
    return adict
def crazy_systems():
    system_list=System.objects.all()
    adict={}
    for e in system_list:
        subunit_composition=e.subunit_composition
        if len(subunit_composition)>3:
            subunit_composition=''.join(sorted(subunit_composition))

            if subunit_composition not in adict:adict[subunit_composition]=1
            else:adict[subunit_composition]=adict[subunit_composition]+1
   # print 'crazy_systems', adict
    return adict
def general_stats():
    M=R=S=0
    M=len(Protein.objects.filter(subunit_kind="M"))
    R=len(Protein.objects.filter(subunit_kind="R"))
    S=len(Protein.objects.filter(subunit_kind="S"))
    X=len(Protein.objects.filter(subunit_kind=""))
#no of genomic clasters of subunit coding genes   
    aDict={}
    system_list=System.objects.all()
    for e in system_list:
        pset= e.protein_set.exclude(subunit_kind="")
        system_length=len(pset)
        if system_length not in aDict.keys():aDict[system_length]=1
        else:aDict[system_length]=aDict[system_length]+1
    return M,R,S,X,aDict
    #how many MRS sububits in the base?
    
    #how many systems with 1 2 3 4 5 6 7 ...sunits
def pairwise_overlap():
    system_list=System.objects.all()
    adict={}
    num_dict={}
    for e in system_list:
        pset= e.protein_set.all()
        previous_prot_mrs=""
        previous_prot_strand=""
        for f in pset:
            current_prot_mrs=f.subunit_kind
            current_prot_strand=f.strand
            if current_prot_mrs !="" and current_prot_mrs !="" and previous_prot_mrs !="" and current_prot_strand==previous_prot_strand:
               '''takes into concideration strand'''
               ms=""
               if current_prot_strand=='-': ms=current_prot_mrs+previous_prot_mrs
               elif  current_prot_strand=='+': ms=previous_prot_mrs+current_prot_mrs
               if ms not in adict: adict[ms]=1
               else: adict[ms]=adict[ms]+1
               #sort out division into particular numbers!!
               margin_left=f.margin_left
               if margin_left>15:margin_left='large'
               if margin_left<-15:margin_left='small'
               if ms not in num_dict: 
                   aux_dict=dict()
                   aux_dict[margin_left]=1
                   num_dict[ms]=aux_dict

               else:
                   aux_dict=num_dict[ms]
                   if margin_left not in  aux_dict.keys(): 
                       aux_dict[margin_left]=1
                   else:
                       aux_dict[margin_left]=aux_dict[margin_left]+1
                   num_dict[ms]=aux_dict
                       
            previous_prot_mrs=current_prot_mrs
            previous_prot_strand=current_prot_strand
    #print 'pairwise_overlap', adict 
    #print 'pairwise_overlap_num_dict', num_dict 
    return adict, num_dict
def mrs_calc():
    system_list=System.objects.all()
    orderMRSdict={}
    for e in system_list:
        strand=set()
        order=''
        #does it have mrs
        subunit_composition=e.subunit_composition
        if 'M' in subunit_composition and 'R' in subunit_composition and 'S' in subunit_composition:
            #does it have 3 prots
            if e.protein_set.all().exclude(system_part='<not>').count()==3:
                pset= e.protein_set.all().exclude(system_part='<not>')
                for f in pset:
                    strand.add(f.strand)
                    order=order+f.subunit_kind
                #is on one strand only 
                if len(strand)==1:
                    #correct for the negative strand
                    if '-' in str(strand):
                        order=order[::-1]
                    #print order
                    if order not in orderMRSdict:orderMRSdict[order]=1
                    else: orderMRSdict[order]= orderMRSdict[order]+1
    return orderMRSdict
def mrs_fam_calc():
    system_list=System.objects.all()
    orderMRSdict={}
    for e in system_list:
        strand=set()
        fam=set()
        order=''
        #does it have mrs
        subunit_composition=e.subunit_composition
        if 'M' in subunit_composition and 'R' in subunit_composition and 'S' in subunit_composition:
            #does it have 3 system prots
            if e.protein_set.all().exclude(system_part='<not>').count()==3:
                pset= e.protein_set.all().exclude(system_part='<not>')
                for f in pset:
                    strand.add(f.strand)
                    order=order+f.subunit_kind
                    fam.add(f.hammer_cluster)
                #is on one strand only and from the same family
                is_1, fam=is_1_fam(fam);
                if len(strand)==1 and is_1==True:
                    print 'fam', fam
                    if '-' in str(strand):
                        order=order[::-1]
                    order=str(fam).replace('(','').replace(')','').replace('[','').replace(']','').replace('u','').replace('\'','').replace('_HMMER','').replace('set','')+'fam_'+order
                    if order not in orderMRSdict:orderMRSdict[order]=1
                    else: orderMRSdict[order]= orderMRSdict[order]+1
    return orderMRSdict
def is_1_fam(fam):
    is_1=False
    if len(fam)==1 and 'D_HMMER' not in fam: is_1= True
    elif len(fam)==2:
        if 'D_HMMER' in fam and 'DH_HMMER' in fam:
            is_1= True
            fam='D_HMMER'
        if 'H_HMMER' in fam and 'DH_HMMER' in fam:
            is_1= True
            fam='H_HMMER'
        if 'C_HMMER' in fam and 'C1_HMMER' in fam:
            is_1= True
            fam='C_HMMER'
    return is_1, fam
    
def process_subunits_order_3elems_onefam():
    comp_dict={}
    comp_fam_dict={}
    subunits_number_dict={} 
    subunits_small_number_dict={} 
    prot_dict={}
    families=['A','B','C','D','E','F','G','H']
    full_protein_list=Protein.objects.all().select_related()
    Protein_list=full_protein_list.exclude(system_part='<not>')
    #System_list=System.objects.all().select_related().filter(subunit_composition__contains='M').filter(subunit_composition__contains='R').filter(subunit_composition__contains='S')
    previous_sys_id=0
    current_sys_id=0
    mrs_composition=family=strand=''
    mrs_ordered_dict={}
    prots_from_previus_system=list()
    for p in  full_protein_list:
        current_sys_id=p.system_id
        if current_sys_id != previous_sys_id:
            #do calculations for previous system
            prot_dict=analyse(prots_from_previus_system,prot_dict)
            #reset prots_from_previus_system
            prots_from_previus_system=list()
            prots_from_previus_system.append(p)
        else:
            prots_from_previus_system.append(p)
        previous_sys_id=current_sys_id
        
    for p in Protein_list:
        current_sys_id=p.system_id
        if current_sys_id != previous_sys_id:
            #do calculations for previous system

            #get data abou the system do the calculation here
            current_system=System.objects.get(pk=current_sys_id)
            fam=is_singlefam(current_system)
            #get all systems that have MRS and 3 or more subunits and defined Fam and count
            compstring=make_compstring(current_system)
            
            if count_subunits_check_MRS(current_system)>3 and fam!=False:
                fill_dict(subunits_number_dict, compstring)
            if count_subunits(current_system)<3:
                fill_dict(subunits_small_number_dict, compstring)
            if is_threeelem_MRS(current_system) and fam!=False:
                comp=current_system.subunit_composition
                if p.strand!='+': #invert sentence
                    comp=comp[::-1]
                comp_dict=fill_dict(comp_dict, comp)
                comp_fam_dict=fill_dict(comp_fam_dict, fam+comp)
        previous_sys_id=current_sys_id
  
    for f in families:
        comp_fam_dict=percentage_fam_dict(comp_fam_dict, f)
    #comp_dict=percentage_dict(comp_dict)   
    final_dict=fuse_and_fill_dict(comp_dict,comp_fam_dict,families)
    subunits_number_dict=percentage_dict(subunits_number_dict)
    subunits_small_number_dict=percentage_dict(subunits_small_number_dict)
    final_dict=fuse_dict(final_dict,subunits_number_dict)
    final_dict=fuse_dict(final_dict,subunits_small_number_dict)
    #print prot_dict
    return final_dict
#ch
def analyse(protList,prot_dict):
    plus_strand=True
    minus_strand=True  
    for index, p in enumerate(protList):
        if p.strand!='+':
            plus_strand=False
        if p.strand!='+':
            minus_strand=False  
    for index, p in enumerate(protList):
        if p.system_part!='<System>' and p.system_part!='<Solitary>' and plus_strand:
            subunit_order= protList[index-1].subunit_kind+p.subunit_kind
            if len(subunit_order)==2:
                margin_left=p.margin_left
                if margin_left>0:
                    margin_left="positive"
                elif margin_left<-10:
                    margin_left="negative"
                #prot_dict=fill_dict(prot_dict,str(margin_left) )
                prot_dict=fill_dict(prot_dict,subunit_order+str(margin_left) )
    return prot_dict
def make_compstring(current_system):
    comp=current_system.subunit_composition
    comp=list(comp)
    comp.sort()
    compstring=''
    for e in comp:
        compstring=compstring+e
    return compstring
def fuse_and_fill_dict(basic_dict, dict1, families):
    for f in families:
        for e in basic_dict:
            if f+e not in dict1:
              
                dict1[f+e]=0
    for e in basic_dict:
        dict1[e]=basic_dict[e]
    return dict1
def fuse_dict(dict, basic_dict):
    for e in basic_dict:
        dict[e]=basic_dict[e]
    return dict

def fill_dict(dict, elem):
    if elem not in dict:
        dict[elem]=1
    else:
        dict[elem]=dict[elem]+1
    return dict
def percentage_fam_dict(dict, fam):
    total=0
    for e in dict:
        if e[0]==fam:
            total=total+dict[e]
    for e in dict:
        if e[0]==fam:
            dict[e]=100*float(dict[e])/total
    return dict
 
def percentage_dict(dict):
    total=0
    for e in dict:
        total=total+dict[e]
    for e in dict:
        dict[e]=100*float(dict[e])/total
    return dict
 
def is_threeelem_MRS(current_system):
    comp=current_system.subunit_composition
    #result = re.match(r'[MRS]', comp)
    if len(comp)==3 and 'M' in comp and 'R' in comp and 'S' in comp:
        #print comp
        return True
    else:
        return False
def count_subunits(current_system):
    comp=current_system.subunit_composition
    return len(comp)
def count_subunits_check_MRS(current_system):
    comp=current_system.subunit_composition
    #result = re.match(r'[MRS]', comp)
    if 'M' in comp and 'R' in comp and 'S' in comp:
        return len(comp)
    else:
        return False
#returns False if not single family
#returns a Family letter if there are 3 elements containing the same letter    
def is_singlefam(current_system):
    family_composition= current_system.family_composition.replace('_','')
    family_composition_dict={}
    for e in family_composition:
        if e not in family_composition_dict:
            family_composition_dict[e]=1
        else:
            family_composition_dict[e]=family_composition_dict[e]+1
    # pick all the families that are repeated 3 times
    family=''
    for e in family_composition_dict:
        if family_composition_dict[e]==3:
            family=e
            return family
    return False
        
def process_subunits_order(mrs_ordered_dict_old,fam_filter, particular_family):
   
    #get all 3 element systems having MRS
    #get all proteins play exclude <not>
    Protein_list=Protein.objects.all().select_related().exclude(system_part='<not>')
    #System_list=System.objects.all().select_related().filter(subunit_composition__contains='M').filter(subunit_composition__contains='R').filter(subunit_composition__contains='S')
    previous_sys_id=0
    mrs_composition=''
    family=''
    strand=''
    mrs_ordered_dict={}
    mrs_ordered_dict[str(particular_family)+'MRS']=0
    mrs_ordered_dict[str(particular_family)+'MSR']=0
    mrs_ordered_dict[str(particular_family)+'RMS']=0
    mrs_ordered_dict[str(particular_family)+'RSM']=0
    mrs_ordered_dict[str(particular_family)+'SMR']=0
    mrs_ordered_dict[str(particular_family)+'SRM']=0
    for p in Protein_list:
        current_sys_id=p.system_id
        if current_sys_id != previous_sys_id:
            #do the calculations
              sparticular_family_condition_pass=False
              if particular_family==False:
                   sparticular_family_condition_pass=True
              elif len(family)>0:
                   if particular_family in family:
                       sparticular_family_condition_pass=True
              
              if fam_filter==True:
                count_family=False 
                if len(set(family))==1 or 'DH' in family or 'C1' in family or 'HD' in family:
                    count_family=True
              else:
                count_family=True  
              
              if 'M' in mrs_composition and 'R' in mrs_composition and 'S' in mrs_composition and len(strand)==3 and count_family and sparticular_family_condition_pass:
                  if strand=='+++' or strand=='---':
                      if strand=='---':
                           mrs_composition=mrs_composition[::-1]
                      if (str(particular_family)+mrs_composition) in mrs_ordered_dict:
                          mrs_ordered_dict[str(particular_family)+mrs_composition]+=1
                      else:
                         # print mrs_composition
                          print family 
                  #reset variable
              else:
                  pass
                 # print 'not '+family
              mrs_composition=''
              strand=''
              family=''
        strand+=p.strand
        family+=p.hammer_cluster.split('_')[0]
        mrs_composition+=p.subunit_kind
        previous_sys_id=current_sys_id
    sum=0
    for e in mrs_ordered_dict:
        sum=sum+mrs_ordered_dict[e]
    for e in mrs_ordered_dict:
        mrs_ordered_dict[e]=100*float(mrs_ordered_dict[e])/sum
        print 100*float(mrs_ordered_dict[e])/sum
    for e in mrs_ordered_dict:
        mrs_ordered_dict_old[e]=mrs_ordered_dict[e]
    return mrs_ordered_dict_old
def process_genomes_name(Genome_list):
    for g in Genome_list:
        g.formatted_name=g.name.replace('_',' ')
       
    
def process_system_kind(p):
    if '<System>' in p.system_part:
            p.system_part='First protein of the genomic cluster of restriction-modification related proteins'
    elif '<middle>' in p.system_part:
            p.system_part='Located In the middle the genomic cluster of restriction-modification related proteins'
    elif '</System>' in p.system_part:
            p.system_part='Last protein of the genomic cluster of restriction-modification related proteins'
    elif '<Solitary>' in p.system_part:
            p.system_part='It is not associated with the genomic cluster of restriction-modification related proteins'
    elif '<not>' in p.system_part:
            p.system_part='It is not restriction-modification related protein'
#seting M R S

def process_subunit_kind(p):           
    if 'M' in p.subunit_kind:
            p.subunit_kind='Methylase'
    elif 'R' in p.subunit_kind:
            p.subunit_kind='Restrictase' 
    elif 'S' in p.subunit_kind:
            p.subunit_kind='Specificity subunit' 
    #cuting out first letter from gene_id  
def process_gene_id(p): 
    p.gene_id= p.gene_id.split('.')
    p.gene_id=p.gene_id[1]

#format HammerCluster
def process_hammer_cluster(p): 
    if p.hammer_cluster!='':
        p.hammer_cluster=p.hammer_cluster.replace('_HMMER','')

#format aa_sequence
def process_aa_sequence(p):
   
    new_aa_sequence=''                    
    for idx, leter in enumerate(p.aa_sequence):
        if idx%80!=0:
            new_aa_sequence=new_aa_sequence+leter
        else:
            new_aa_sequence=new_aa_sequence+' '+leter
    p.aa_sequence=new_aa_sequence

#seting DNA piece Name    
def process_dnapiece_name(p):
    p.system.dnapiece.name=p.system.dnapiece.name.split('.')
    p.system.dnapiece.name=p.system.dnapiece.name[0]
def process_genome_name(p):
    p.system.dnapiece.genome.name=p.system.dnapiece.genome.name.replace('_',' ')
    
def create_next(p):
    p.next=str(p.id+1)

def create_previous(p):
    if p.gene_id !=0:
        p.previous=str(p.id-1) 