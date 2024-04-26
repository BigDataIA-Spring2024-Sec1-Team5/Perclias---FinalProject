from pydantic import BaseModel, constr, Field, field_validator
import pandas as pd

class MedicalArticle(BaseModel):
   title: constr(strip_whitespace=True, min_length=3, max_length=100) = Field(...)
   content: constr(strip_whitespace=True, min_length=500) = Field(...)

   @field_validator('title', 'content')
   def check_not_empty(cls, v, field):
       if len(v.strip()) == 0:
           raise ValueError(f"{field.name} must not be empty or just whitespace")
       return v

def validate_medical_data(file_path):
   data = pd.read_csv(file_path)
   validated_data = []
   errors = []
   for index, row in data.iterrows():
       try:
           article = MedicalArticle(title=row['Title'], content=row['Content'])
           validated_data.append(article)
       except Exception as e:
           errors.append({'index': index, 'error': str(e)})
   return validated_data, errors

def validation_task(file_path):
   validated_data, validation_errors = validate_medical_data(file_path)
   print("Number of rows with valid data:", len(validated_data))
   print("Number of validation errors:", len(validation_errors))