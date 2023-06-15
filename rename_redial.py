# coding: utf-8
import os, glob,sys
files = glob.glob('./*.pkl')
import json
model_info = json.load(open('../models_and_best_model.json', 'r'))
model_shortcut = json.load(open('../model_shortcut_to_fullform.json', 'r'))    
import json
model_info = json.load(open('../models_and_best_model.json', 'r'))
count = 0
name = []
for f in files:
    f = os.path.basename(f)
    fp_name = f.split('-')[0]
    md_name = "-".join(f.split('-')[:-1][1:])
    if md_name =='cytotox':
        md_name2 = 'Tox'
    elif md_name == 'CPE':
        md_name2 = 'Act'
    elif md_name == 'CoV1-PPE':
        md_name2 = 'CoVPPE'
    elif md_name == 'CoV1-PPE_cs':
        md_name2 = 'CoVPPEcs'
    elif md_name == '3CL':
        md_name2 = '3CLEnzymatic'
    elif md_name == 'ACE2':
        md_name2 = 'ACE2Enzymatic'
    elif md_name == 'MERS-PPE':
        md_name2 = 'MERSPPE'
    elif md_name == 'MERS-PPE_cs':
        md_name2 = 'MERSPPEcs'
    elif md_name == 'AlphaLISA':
        md_name2 = 'AlphaLisa'
    else:
        md_name2 = md_name
    print(md_name, md_name2) 
    if fp_name == 'tpatf':
        temp_name = md_name2+'Topo'
        best_model = model_info['pharmacophore'][md_name]
    elif fp_name == 'rdkDes':
        temp_name = md_name2+'Des'
        best_model = model_info['rdkitDescriptors'][md_name]
    elif fp_name == 'volsurf':
        temp_name = md_name2+'Vsf'
        best_model = model_info['volsurf'][md_name]
    else:
        temp_name = md_name2+'FP'
        best_model = model_info['fingerprints'][md_name]
    
    best_model2 = model_shortcut[best_model]
    final_name = temp_name+'-'+fp_name+'-'+best_model2+'_best.pkl'
    #print(f, final_name)
    count+=1
    name.append(final_name)
    os.rename(f,final_name)
print('Total count ', count)
print(sorted(name))
print('Total uniq', len(set(name)))
