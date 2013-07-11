from models import Genome, DNAPiece, System, Protein,System, ProteinForm 
from django.http import HttpResponse
import decimal
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import proteinAttributesModifier 
from itertools import chain
# Create your views here.
from models import Genome, DNAPiece, System, Protein
from django.http import HttpResponse
import decimal
import helpers
from django.db.models import Q
from django.db.models import Count
import csv
from django.http import HttpResponse
import json


def draw_rna(request):
    list_of_coordinates=[(498, 837),
                         (391, 704),
                         (384, 650),
                         (377, 607),
                         (370, 554),
                         (364, 500)]
    return render_to_response('obsolete/eps_drowing_test.html', {'list_of_coordinates': list_of_coordinates}, context_instance=RequestContext(request))

def results_to_text_file(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=somefilename.txt'
    dna = get_object_or_404(DNAPiece, pk=2)
    response.write(dna)
    response.write(dna)
    return response

def results_to_csv_file(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
def calculate_order(request):
   
    order_MRS_dict=proteinAttributesModifier.mrs_calc()
    order_MRS_fam_dict=proteinAttributesModifier.mrs_fam_calc()
    solitary_dict=proteinAttributesModifier.solitary_subunis()
    crazy_dict=proteinAttributesModifier.crazy_systems()
    pairwise_overlap, pairwise_overlap_num_dict=proteinAttributesModifier.pairwise_overlap()
    
    M,R,S,X,length_dict=proteinAttributesModifier.general_stats()
    print M,R,S,X
    print length_dict
    results_dict=dict()
    '''
    >>> import json
    >>> data=[{'total': 1744, 'name': u'x'}, {'total': 13, 'name': u'm'}, {'total': 126, 'name': u'n'}]
    >>> json.dumps([i.values()[::-1] for i in data])
    '[["x", 1744], ["m", 13], ["n", 126]]'
    >>> 
    [{ country: "USA", visits: 4252 },
    {"RMS": 177, "RSM": 77, "MSR": 517, "SMR": 2, "MRS": 3, "SRM": 1} 
    [{ subunits: "RMS", systems: 177 },
    '''
    #order_MRS_dict=json.dumps(order_MRS_dict) 

    results_dict['order_MRS_dict']=proteinAttributesModifier.string_to_json(order_MRS_dict,'country','visits', True,False)
    results_dict['order_MRS_fam_dict']=proteinAttributesModifier.string_to_json(order_MRS_fam_dict,'country','visits',True, False)
    results_dict['solitary_dict']=proteinAttributesModifier.string_to_json(solitary_dict,'country','visits', False,True)
    results_dict['crazy_dict']=proteinAttributesModifier.string_to_json(crazy_dict,'country','visits', False, True)
    results_dict['pairwise_overlap']=proteinAttributesModifier.string_to_json(pairwise_overlap,'country','visits', False, True)
    results_dict['pairwise_overlap_num_dict']=json.dumps(pairwise_overlap_num_dict)
    results_dict['length_dict']=proteinAttributesModifier.string_to_json(length_dict,'country','visits', False, True)
    results_dict['M']=M
    results_dict['R']=R
    results_dict['S']=S
    results_dict['X']=X
    #results_dict['order_MRS_dict']=order_MRS_dict
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,True,False)
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,True, False)
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'A')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'B')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'C')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'C1')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'D')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'E')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'F')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'G')
 #   mrs_ordered_dict=proteinAttributesModifier.process_subunits_order(mrs_ordered_dict,False,'H')
 #   results_dict=proteinAttributesModifier.process_subunits_order_3elems_onefam()

   # print mrs_ordered_dict   
    
    return render_to_response('typei/graphs.html', results_dict, context_instance=RequestContext(request))

def detailedProtein(request, pk):
    p = get_object_or_404(Protein, pk=pk)
    proteinAttributesModifier.process_system_kind(p)
    proteinAttributesModifier.process_subunit_kind(p)
    proteinAttributesModifier.process_gene_id(p) 
    proteinAttributesModifier.process_hammer_cluster(p)
    proteinAttributesModifier.process_aa_sequence(p)
    proteinAttributesModifier.process_dnapiece_name(p)
    proteinAttributesModifier.process_genome_name(p)
    proteinAttributesModifier.create_next(p)
    proteinAttributesModifier.create_previous(p)
    return render_to_response('typei/proteinDetail.html', {'protein': p}, context_instance=RequestContext(request))


def genome(request, pk):
    g = get_object_or_404(Genome, pk=pk)
    #get allproteins from this genome  
    return render_to_response('typei/genome.html', {'genome': g}, context_instance=RequestContext(request))

def dna(request, pk):
    dna = get_object_or_404(DNAPiece, pk=pk)
    #get allproteins from this genome
    return render_to_response('typei/dna.html', {'dna': dna}, context_instance=RequestContext(request))
def system(request, pk):
    s = get_object_or_404(System, pk=pk)
    #get allproteins from this genome
    return render_to_response('typei/system.html', {'system': s}, context_instance=RequestContext(request))

def home(request):
   return render_to_response('typei/home.html', context_instance=RequestContext(request))
def stats(request):
   return render_to_response('typei/stats.html', context_instance=RequestContext(request))
def contact(request):
   return render_to_response('typei/contact.html', context_instance=RequestContext(request))
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def paginated_browse(request):
    Genome_lists = Genome.objects.all().select_related().order_by('name')
    proteinAttributesModifier.process_genomes_name(Genome_lists)
    paginator = Paginator(Genome_lists, 200) # Show 25 contacts per page

    page = int(request.GET.get('page', '1'))
    try:
        genomes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        genomes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        genomes = paginator.page(paginator.num_pages)
        
    return render_to_response('typei/paginated_browse.html', {'Genome_list': genomes}, context_instance=RequestContext(request))
def browse(request):
    
    Genome_lists = Genome.objects.all().select_related().order_by('name')
    proteinAttributesModifier.process_genomes_name(Genome_lists)
    paginator = Paginator(Genome_lists, 5000) # Show 25 contacts per page

    page = int(request.GET.get('page', '1'))
    try:
        genomes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        genomes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        genomes = paginator.page(paginator.num_pages)
        
    return render_to_response('typei/browse.html', {'Genome_list': genomes}, context_instance=RequestContext(request))

def listing(request):
    contact_list = Genome.objects.all().select_related().order_by('name')
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

   
    page = int(request.GET.get('page', '1'))
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('typei/listing.html', {"contacts": contacts})
def listdisplay(request):
    
    Genome_list = Genome.objects.all().select_related().order_by('name')
  
    #template aDictionary requestContext
    return render_to_response('typei/list.html', {'Genome_list': Genome_list}, context_instance=RequestContext(request))

def basic_browse(request):
    Genome_list = Genome.objects.all().select_related().order_by('name')
    proteinAttributesModifier.process_genomes_name(Genome_list)
    #template aDictionary requestContext
    return render_to_response('typei/base_browse.html', {'Genome_list': Genome_list}, context_instance=RequestContext(request))

def browse_by_family(request):
    System_list=System.objects.all().select_related().filter(subunit_family_composition__contains='E')
     # proteinAttributesModifier.process_genomes_name(Genome_list)
    #template aDictionary requestContext
    return render_to_response('typei/search.html', {'System_list': System_list}, context_instance=RequestContext(request))
def change_any_to_empty_string(s):
    if str(s) =='any':
        s=str('')
    return str(s)

def set_condition(Mnum, system, expected_num):
    Mcondition=False
    if 'or' not in Mnum and expected_num == int(Mnum):
        Mcondition = True
    elif 'or' in Mnum and expected_num >= int(Mnum.split('_or_')[0]):
        Mcondition = True
    return Mcondition

def formtest(request):
    Mfam=Rfam=Sfam=Mnum=Rnum=Snum='xx'
    if 'filter' in request.POST:
        Mfam=request.POST['Mfam']
        Mnum=request.POST['Mnum']
        Rnum=request.POST['Rnum']
        Rfam=request.POST['Rfam']
        Snum=request.POST['Snum']
        Sfam=request.POST['Sfam']
        print 'filter'
      
    #System_list=System.objects.all().filter(subunit_family_composition__contains='SC')
    if Sfam!='':
        SSfam='S'+Sfam
    else:
        SSfam=''
    if Sfam!='':
        MMfam='M'+Mfam
    else:
        MMfam=''
    if Sfam!='':    
        RRfam='R'+Rfam
    else:
        RRfam=''
    System_list=System.objects.filter(
    Q(subunit_family_composition__contains=SSfam),
    Q(subunit_family_composition__contains=MMfam),
    Q(subunit_family_composition__contains=RRfam)
    )
    matching_systems=0
    for system in System_list:
        system.m_num=system.subunit_family_composition.count('M')
        system.r_num=system.subunit_family_composition.count('R')
        system.s_num=system.subunit_family_composition.count('S')
        Mcondition=Rcondition=Scondition=False
        Mcondition = set_condition(Mnum, system, system.m_num)
        Rcondition = set_condition(Rnum, system, system.r_num)
        Scondition = set_condition(Snum, system, system.s_num)
        if Mcondition and Rcondition and Scondition:
            system.display=True
            matching_systems=matching_systems+1
        else:
            system.display=False
        
           # Mnum=
     # Each publisher, each with a count of books as a "num_books" attribute.

      
   # proteinAttributesModifier.process_genomes_name(Genome_list)
    #template aDictionary requestContext
    return render_to_response('typei/formtest.html', {'System_list': System_list, 'matching_systems':matching_systems}, context_instance=RequestContext(request))

 
def loadGenome(request):
    f = open('C:/Users/anna/Desktop/Doktorat/typeii/src/typeii/sourceData/proteins_new.csv')
    genomes = []
    for line in f:
        p = line.split(',')
        genome = p[0].replace('"', '')
        if genome in genomes or genome == 'Genome' or genome == 'x':
            pass
        else:
            genomes.append(genome)
    for record in genomes:
        print (record)
        g = Genome(name=record)
        try:
            g.save()
        except Exception:
            print ('Already exists.')
    return HttpResponse('Action completed.')

def loadPiece(request):
    f = open('C:/Users/anna/Desktop/Doktorat/typeii/src/typeii/sourceData/proteins_new.csv')
    pieces = []
    genomes = Genome.objects.all()
    for line in f:
        p = line.split(',')
        piece = p[2].replace('"', '')
        g = p[0].replace('"', '')
        if piece in pieces or piece == 'DNApiece':
            pass
        else:
            pieces.append(piece)
            print(piece)
            for record in genomes:
                if record.name == g:
                    """'genome' variable in DNAPiece object must be Genome object, therefore you have to
                    find Genome object of corresponding 'name' to the given DNAPiece genome name"""
                    dnap = DNAPiece(genome=record, name=piece)
                    try:
                        dnap.save()
                    except Exception:
                        print ('Already exists.')
    return HttpResponse('Action complete.')

def loadSystem(request):
    f = open('C:/Users/anna/Desktop/Doktorat/typeii/src/typeii/sourceData/proteins_new.csv')
    systems = []
    first_line = 1
    pieces = DNAPiece.objects.all()
    for line in f:
        p = line.split(',')
        system_number = p[3]
        if system_number in systems or first_line == 1:
            first_line = 0
            pass
        else:
            dnapiece = p[2].replace('"', '')
            subunit_composition = p[8].replace('"', '')
            family_composition = p[9].replace('"', '')
            split_family = family_composition.split('_')
            merge = ''
            for idx, char in enumerate(subunit_composition):
                merge += char
                merge += split_family[idx]+'_'
            subunit_family_composition = merge
            system_kind = p[14].replace('"', '')
            real_name = ''
            print (subunit_composition + ' ' + family_composition + ' ' + subunit_family_composition + ' ' + 
               system_kind + ' ' + real_name)
            systems.append(system_number)
            for record in pieces:
                if record.name == dnapiece:
                    s = System(dnapiece=record, subunit_composition=subunit_composition, family_composition=family_composition, 
                               subunit_family_composition=subunit_family_composition, system_kind=system_kind, 
                               real_name=real_name)
                    s.save()
                    print ('System added')
    return HttpResponse('Action complete.')

def loadProtein(request):
    f = open('C:/Users/anna/Desktop/Doktorat/typeii/src/typeii/sourceData/nonsystemalso_new.csv')
    proteins = []
    headers = 2
    '''#uncomment to use test mode (upload only 5 records)
    temp = 40#test'''
    
    # possibly needed to indicate protein affiliation
    #genomes = Genome.objects.all()
    #pieces = DNAPiece.objects.all()
    systems = System.objects.all()
    for line in f:
        data = line.split(',')
        gene_id = data[0].replace('"', '')
        if gene_id in proteins or headers != 0:
            headers -= 1
            pass
        else:
            system = int(data[4].replace('"', ''))
            genome_location = data[8].replace('"', '')
            if data[9].replace('"', '') == '+':
                strand = '+'
            else:
                strand = '-'
            margin_left = int(data[10].replace('"', ''))
            system_part = data[11].replace('"', '')
            clans_cluster = '' #fixed value till data available
            hammer_cluster = data[12].replace('"', '')
            subunit_kind = data[13].replace('"', '')
            dna_length = int(data[15].replace('"', ''))
            aa_sequence = data[17].replace('"', '')
            hh_pfam_id = data[18].replace('"', '')
            hh_pfam_short_desc = data[19].replace('"', '')
            hh_probability_raw = data[20].replace('"','')
            if hh_probability_raw != '':
                hh_probability = decimal.Decimal(hh_probability_raw)
            else:
                hh_probability = decimal.Decimal(0.0) #default for records without hh value
            hh_probability.quantize(decimal.Decimal('.01'))
            hh_e_value = data[21].replace('"', '')
            hh_pfam_desc = data[22].replace('"', '')
            m_probability = 0 #fixed value till data from Vilno
            r_probability = 0 #fixed value till data from Vilno
            s_probability = 0 #fixed value till data from Vilno
            print (gene_id)
            proteins.append(gene_id)
            for record in systems:
                if record.id == system:
                    #uncomment for verbose upload
                    print(record.id, gene_id + ' ' + genome_location + ' ' +
                                strand, margin_left, system_part + ' ' +
                                clans_cluster + ' ' + hammer_cluster + ' ' +
                                subunit_kind, dna_length, aa_sequence + ' ' +
                                hh_pfam_id + ' ' + hh_pfam_short_desc,
                                hh_probability, hh_e_value + ' ' +
                                hh_pfam_desc, m_probability,
                                r_probability, s_probability)
                    p = Protein(system=record, gene_id=gene_id, genome_location=genome_location,
                                strand=strand, margin_left=margin_left, system_part=system_part,
                                clans_cluster=clans_cluster, hammer_cluster=hammer_cluster,
                                subunit_kind=subunit_kind, dna_length=dna_length, aa_sequence=aa_sequence,
                                hh_pfam_id=hh_pfam_id, hh_pfam_short_desc=hh_pfam_short_desc,
                                hh_probability=hh_probability, hh_e_value=hh_e_value,
                                hh_pfam_desc=hh_pfam_desc, m_probability=m_probability,
                                r_probability=r_probability, s_probability=s_probability)
                    p.save()
                    print('Protein appended.')
                    '''#uncomment to use test mode (upload only 5 records)
                    temp -= 1#test
        if temp == 0:#test
            break#test'''
    return HttpResponse('Download complete.')
    
def searchView(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(gene_id__icontains=query) |
            Q(system_part__icontains=query)
            )
        result = Protein.objects.filter(qset).distinct()
    else:
        result = []
    return render_to_response('search_protein.html', {
                'result': result,
                'query': query
                }) 
    
def searchAll(request):
    query = request.GET
    form = ProteinForm(request.GET, auto_id=False)
    filled = []
    if query:
        qset = (
            Q(gene_id__icontains=query['gene_id']) &
            Q(margin_left__icontains=query['margin_left']) &
            Q(system_part__icontains=query['system_part']) &
            Q(hammer_cluster__icontains=query['hammer_cluster']) &
            Q(subunit_kind__icontains=query['subunit_kind']) &
            Q(aa_sequence__icontains=query['aa_sequence']) &
            Q(hh_pfam_id__icontains=query['hh_pfam_id']) &
            Q(hh_pfam_desc__icontains=query['hh_pfam_desc'])
            )
        if query['genome'] != '':
            qset.add(Q(system__dnapiece__genome__id__exact=query['genome']), Q.AND)
        if query['dnapiece'] != '':
            qset.add(Q(system__dnapiece__id__exact=query['dnapiece']), Q.AND)
        if query['system'] != '':
            qset.add(Q(system__id__exact=query['system']), Q.AND)
        result = Protein.objects.filter(qset).distinct()
        for field in query.itervalues():
            if field != '':
                filled.append(field)
    else:
        result = []
    return render_to_response('typei/search.html', {
                'result': result,
                'query': query,
                'form': form,
                'filled': filled
                }, context_instance=RequestContext(request))
def searchSys(request):
    form = ProteinForm(request.GET, auto_id=False)
    filled = []
    query = request.POST
    if query:
        Mnum = query['Mnum']
        Rnum = query['Rnum']
        Snum = query['Snum']
        Mfam = query['Mfam']
        Rfam = query['Rfam']
        Sfam = query['Sfam']
        '''   qset = (
            Q(gene_id__icontains=query['gene_id']) &
            Q(margin_left__icontains=query['margin_left'])
            )
            '''
     #  result = System.objects.filter(system_id__icontains='9').distinct().protein_set.objects.all()
       # system=System.objects.get(id=1)
        systems=System.objects.all()
        selected_systems=list()
        for system in systems:
            Mnum_found=Snum_found=Rnum_found=0
            Mfam_found=Rfam_found=Sfam_found=set()
            proteins_within_system= system.protein_set.exclude(system_part= '<not>')
            for protein in proteins_within_system:
                print protein.hammer_cluster
                if protein.subunit_kind =='M':
                    Mnum_found+=1
                    Mfam_found.add(protein.hammer_cluster.replace('_HMMER',''))
                elif  protein.subunit_kind =='R':
                    Rnum_found+=1
                    Rfam_found.add(protein.hammer_cluster.replace('_HMMER',''))
                elif  protein.subunit_kind =='S':
                    Snum_found+=1
                    Sfam_found.add(protein.hammer_cluster.replace('_HMMER',''))
            # has correct number of M subunits
            Mpass=helpers.passSubunitCondition(Mnum, Mnum_found)
            Rpass=helpers.passSubunitCondition(Rnum, Rnum_found)
            Spass=helpers.passSubunitCondition(Snum, Snum_found)
            MfamPass=helpers.passSubunitFamCondition(Mfam, Mfam_found)
            RfamPass=helpers.passSubunitFamCondition(Rfam, Rfam_found)
            SfamPass=helpers.passSubunitFamCondition(Sfam, Sfam_found)
            PassLiss=set({Mpass,Rpass,Spass,MfamPass,RfamPass,SfamPass})
            print PassLiss
            if False not in PassLiss: selected_systems.append(system)
        print len(selected_systems)
        for field in query.itervalues():
            if field != '':
                filled.append(field)
    else:
        result = []
    return render_to_response('typei/search.html', {
                'result': result,
                'query': query,
                'form': form,
                'filled': filled
                }, context_instance=RequestContext(request))