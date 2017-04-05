from csv import DictReader 
from django.forms import ModelForm

def csv_import_to_model(csvfile, modelClass, csvFields, keyFields=[], booleanFields=[], mapFunctions={}):
    csv_fh = open(csvfile,'r')
    reader = DictReader(csv_fh)

    class LoadingForm(ModelForm):
        class Meta:
            model = modelClass
            fields = csvFields
    
    loadcounts = { 'insert' : 0, 'update' : 0, 'failed': 0 }
      
    for row in reader:
        handle_booleans(row, booleanFields)
        
        for (field, map) in mapFunctions.items():
            row[field] = map(row[field])
            
        instance = instance_for_row(row, modelClass, keyFields)

        form = LoadingForm(row, instance=instance)

        if form.is_valid():
            loadcounts['insert' if instance == None else 'update'] += 1
            form.save()
        else: 
            loadcounts['failed'] += 1
            print 'Failed to load: %s' % row['name']
            print_form_errors(form)

    print '%s load complete: %i new, %i updated, %i failed to load' % (modelClass.__name__, loadcounts['insert'], loadcounts['update'], loadcounts['failed'])           
    csv_fh.close()

def migration_map_fk(apps, app_name, model, fk_field):
    ModelClass = apps.get_model(app_name, model)

    def map_fk(fk):
        kwargs={fk_field : fk}

        try:
            return ModelClass.objects.get(**kwargs).id
        except ModelClass.DoesNotExist:
            return None

    return map_fk

def instance_for_row(row, model, keyFields):
    try:
        keys = dict([(k, row[k]) for k in keyFields])
        return model.objects.get(**keys)
    except model.DoesNotExist:
        return None    

def handle_booleans(row, fields):   
    for boolean in fields:
        row[boolean] = (row[boolean].upper() =='TRUE')
    
def print_form_errors(form):
    for error in form.non_field_errors():
        print "\t%s" % error
    for field, errorList in form.errors.items():
        for error in errorList:
            print "\t%s:\t%s" % (field, error)
