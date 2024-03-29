# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-18 20:52
from __future__ import unicode_literals

from django.db import migrations

data = {
    'Sexual and reproductive health': [
        'Comprehensive sexuality education',
        'Contraception/family planning',
        'Safe abortion care',
        'Infertility',
        'Female genital mutilation',
        'Sexually Transmitted Infections (STIs)',
        'HIV/AIDS',
        'Human papillomavirus (HPV) and cervical cancer',
        'Other sexual and reproductive health',
    ],
    'Maternal health': [
        'Pregnancy/antenatal care',
        'Birth preparedness',
        'Intrapartum care (labor and delivery)',
        'Postpartum care',
        'Elimination of Mother to Child Transmission (eMTCT) of HIV/AIDs and Syphilis  (EMTCT/PMTCT)',
        'Maternal Vaccination / Immunization',
        'Other maternal health',
    ],
    'Newborn and Child Health': [
        'Postnatal/newborn care',
        'Childhood vaccinations / immunization',
        'Breastfeeding',
    ],
    'Elimination of Mother to Child Transmission (eMTCT) of HIV/AIDs and Syphilis (EMTCT/PMTCT)': [
        'Integrated Management of Newborn and Childhood Infections (IMNCI)',
        'Malformations/birth defects',
        'Child growth and development',
        'Child abuse',
        'Infant/child nutrition and micronutrient deficiency',
        'Other newborn and child health',
    ],
    'Adolescent and Youth Health': [
        'School-based health programs',
        'Child marriage',
        'Youth friendly services',
        'Life-skills training',
        'Adolescents and sexual and reproductive health',
        'Adolescents and communicable diseases',
        'Adolescents and non-communicable diseases',
        'Adolescents and mental health',
        'Adolescents and violence',
        'Other adolescent and youth health',
    ],
    'Civil registration and vital statistics': [
        'Birth events',
        'Death events',
        'Registration of clients and demographic information',
        'Other civil registration and vital statistics',
    ],
    'Infectious diseases (non-vector borne)': [
        'Tuberculosis',
        'Hepatitis',
        'Meningitis',
        'Measles',
        'Influenza',
        'Polio',
        'Pneumonia',
        'Ebola Viral Disease (EVD)',
        'Other hemorrhagic fever (e.g. Lassa fever)',
        'Other infectious diseases (non-vector borne)',
    ],
    'Non-communicable diseases': [
        'Cancer',
        'Diabetes',
        'Hypertension',
        'Cardiovascular disease',
        'Tobacco use',
        'Alcohol use',
        'Substance abuse',
        'Oral health',
        'Other non-communicable diseases',
    ],
    'Vector-borne diseases (not listed under Neglected Tropical Diseases (NTDs)': [
        'Chikungunya',
        'Malaria',
        'Rift Valley fever',
        'Yellow fever',
        'Japanese encephalitis',
        'West Nile fever',
        'Sandfly fever (phlebotomus fever)',
        'Rickettsiosis',
        'Zika',
        'Other vector borne',
    ],
    'Neglected Tropical Diseases (NTDs)': [
        'Dengue',
        'Rabies',
        'Trachoma',
        'Leprosy',
        'Chagas',
        'Human African trypanosomiasis (sleeping sickness)',
        'Leishmaniases',
        'Dracunculiasis (guinea-worm disease)',
        'Echinococcosis',
        'Foodborne trematodiases',
        'Lymphatic filariasis',
        'Onchocerciasis (river blindness)',
        'Soil-transmitted helminthiasis (e.g. whipworm, hookworms, roundworms)',
        'Mycetoma',
        'Schistosomiasis (bilharziasis)',
        'Residual spraying',
        'Other neglected tropical diseases',
    ],
    'Nutrition and metabolic disorders': [
        'Malnutrition',
        'Micronutrient deficiency',
        'Obesity',
        'Metabolic and endocrine disorders',
        'Diet',
        'Other nutrition and metabolic disorders',
    ],
    'Other chronic conditions and disabilities': [
        'Diseases of the digestive system',
        'Diseases of the respiratory system  (e.g. asthma, COPD)',
        'Diseases of the skin and subcutaneous tissue (e.g. dermatitis, hair loss)',
        'Diseases of the musculoskeletal system and connective tissue',
        'Diseases of the nervous system (e.g. epilepsy, cerebral palsy)',
        'Diseases of the kidney and the urinary system',
        'Diseases of the eye and vision loss (e.g. cataracts, vision loss)',
        'Diseases of the ear and hearing loss',
        'Learning and Developmental Disabilities',
        'Other chronic conditions and disabilities',
    ],
    'Humanitarian health': [
        'Migrant populations',
        'Communicable diseases in humanitarian settings',
        'Sexual and Reproductive health in humanitarian settings',
        'Other humanitarian health',
    ],
    'Violence': [
        'Sexual violence',
        'Physical violence',
        'Emotional violence',
        'Other violence',
    ],
    'Injury prevention and management': [
        'Road traffic injuries',
        'Poisonings',
        'Falls',
        'Burns',
        'Drowning',
        'Suicide',
        'Occupational health',
        'Other injury prevention and management',
    ],
    'Water Sanitation and Hygiene (WASH)': [
        'Management of diarrheal diseases',
        'Handwashing',
        'Hygiene education',
        'Water treatment',
        'Other WASH',
    ],
    'Environmental Health': [
        'Outdoor air pollution',
        'Indoor air pollution',
        'Chemical safety',
        'Climate change impact on health',
        'Water treatment (see also under Water Sanitation and Hygiene (WASH)',
        'Natural disaster risk mitigation and response',
        'Other Environmental',
    ],
    'Wellness and Mental Health': [
        'Physical Activity',
        'Substance abuse',
        'Mental health',
        'Ageing',
        'Other wellness and mental health',
    ],
    'Cross Cutting': [
        'Infection Prevention Control',
        'Blood Safety',
        'Immunizations',
        'Health Promotion',
        'Emergency Medical Services',
        'Preparedness',
        'Surveillance',
        'Other cross cutting',
    ]
}


def make_dynamic(apps, schema_editor):
    HealthCategory = apps.get_model('project', 'HealthCategory')
    HealthFocusArea = apps.get_model('project', 'HealthFocusArea')
    for category, items in data.items():
        hc = HealthCategory.objects.create(name=category)
        for hfa in items:
            HealthFocusArea.objects.create(health_category=hc, name=hfa)


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_healthcategory_healthfocusarea'),
    ]

    operations = [
        migrations.RunPython(make_dynamic),
    ]
