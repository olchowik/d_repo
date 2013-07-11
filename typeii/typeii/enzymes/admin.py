from models import Genome, DNAPiece, System, Protein
from django.contrib import admin
from django.forms import TextInput
from django.db import models


class ProteinAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})}
        }
    fieldsets = [
        ('General data',      {'fields': ['system', ('gene_id', 'genome_location', 'strand', 'margin_left'),
                                         ('system_part', 'subunit_kind'),
                                         ('clans_cluster', 'hammer_cluster')]}),
        ('Sequence', {'fields': ['dna_length', 'aa_sequence'], 'classes': ['collapse']}),
        ('Pfam data', {'fields': ['hh_pfam_id', 'hh_pfam_short_desc', 'hh_probability',
                                   'hh_e_value', 'hh_pfam_desc'], 'classes': ['collapse']}),
        ('Probabilities', {'fields': ['m_probability', 'r_probability',
                                       's_probability'], 'classes': ['collapse']}),
    ]

admin.site.register(Genome)
admin.site.register(DNAPiece)
admin.site.register(System)
admin.site.register(Protein, ProteinAdmin)