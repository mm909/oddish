# oddish.health


## AppleHealthKit 

### Metadata
The only metadata we collect from the export.xml is the export date
```python
# Sample Metadata (AppleHealthKit.metadata)
{
    'export_date': '2024-08-11 21:34:30 -0700'
}
```

### Characteristics
[Here](https://developer.apple.com/documentation/healthkit/hkhealthstore#1676877) you can find a full list of AppleHealthKit characteristics
```python
# Sample characteristics (AppleHealthKit.characteristics)
{
    'DateOfBirth': '2000-01-01',
    'BiologicalSex': 'HKBiologicalSexMale',
    'BloodType': 'HKBloodTypeNotSet',
    'FitzpatrickSkinType': 'HKFitzpatrickSkinTypeNotSet',
    'CardioFitnessMedicationsUse': 'None'
}
```

### Quantities
There are two different types of quantities found in AppleHealthKit records 
- [HKQuantityTypeIdentifier](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier)
- [HKCategoryTypeIdentifier](https://developer.apple.com/documentation/healthkit/hkcategorytypeidentifier)

Here is a sample list of quantities found while processing the export.xml
```python
quantities = [
    'Height',
    'BodyMass',
    'HeartRate',
    'RespiratoryRate',
    'StepCount',
    'DistanceWalkingRunning',
    'BasalEnergyBurned',
    'ActiveEnergyBurned',
    'FlightsClimbed',
    'AppleExerciseTime',
    'WaistCircumference',
    'RestingHeartRate',
    'VO2Max',
    'WalkingHeartRateAverage',
    'EnvironmentalAudioExposure',
    'HeadphoneAudioExposure',
    'WalkingDoubleSupportPercentage',
    'SixMinuteWalkTestDistance',
    'AppleStandTime',
    'WalkingSpeed',
    'WalkingStepLength',
    'WalkingAsymmetryPercentage',
    'StairAscentSpeed',
    'StairDescentSpeed',
    'SleepDurationGoal',
    'AppleWalkingSteadiness',
    'SleepAnalysis',
    'AppleStandHour',
    'HeartRateVariabilitySDNN'
]
```

Each quantity comes from a record in the xml
```xml
 <Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Mikian’s Apple Watch" sourceVersion="7.6.2" device="&lt;&lt;HKDevice: 0x282d03020&gt;, name:Apple Watch, manufacturer:Apple Inc., model:Watch, hardware:Watch5,4, software:7.6.2&gt;" unit="count/min" creationDate="2021-12-11 18:04:48 -0700" startDate="2021-12-11 18:04:47 -0700" endDate="2021-12-11 18:04:47 -0700" value="92">
  <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" value="2"/>
 </Record>
```

In this case we store the record attributes in a dataframe and ignore any MetadataEntry inside the record. Note that device isn't always present in every record type.

```python
quantities['HeartRate'].columns
'type',
'sourceName',
'sourceVersion',
'device',
'unit',
'creationDate',
'startDate',
'endDate',
'value'
```

### Workout
There are many different types of workouts defined with [HKWorkoutActivityType](https://developer.apple.com/documentation/healthkit/hkworkoutactivitytype)

Here is a sample list of workouts found while processing the export.xml
```python
workout_types = [
    'CardioDance',
    'Walking',
    'Swimming',
    'Cycling',
    'Running',
    'Basketball',
    'FunctionalStrengthTraining',
    'Pickleball',
    'Other',
    'StairClimbing'
]
```

Each workout has the following attributes as defined by the DTD
```
workoutActivityType  
duration             
durationUnit         
totalDistance        
totalDistanceUnit    
totalEnergyBurned    
totalEnergyBurnedUnit
sourceName           
sourceVersion        
device               
creationDate         
startDate            
endDate   
```

Here is a abbreviated sample workout xml
```
 <Workout workoutActivityType="HKWorkoutActivityTypeWalking" duration="123.4971656322479" durationUnit="min" sourceName="Oddish’s Apple Watch" sourceVersion="7.3.3" device="&lt;&lt;HKDevice: 0x282df23f0&gt;, name:Apple Watch, manufacturer:Apple Inc., model:Watch, hardware:Watch5,4, software:7.3.3&gt;" creationDate="2021-06-18 07:36:53 -0700" startDate="2021-06-18 05:33:19 -0700" endDate="2021-06-18 07:36:49 -0700">
  <MetadataEntry key="HKIndoorWorkout" value="0"/>
  <MetadataEntry key="HKAverageMETs" value="4.85252 kcal/hr·kg"/>
  <MetadataEntry key="HKWeatherTemperature" value="91.4 degF"/>
  <MetadataEntry key="HKWeatherHumidity" value="1500 %"/>
  <MetadataEntry key="HKTimeZone" value="America/Los_Angeles"/>
  <MetadataEntry key="HKElevationAscended" value="5348 cm"/>
  <WorkoutEvent type="HKWorkoutEventTypeSegment" date="2021-06-18 05:33:19 -0700" duration="12.20846013824145" durationUnit="min"/>
  <WorkoutEvent type="HKWorkoutEventTypeSegment" date="2021-06-18 05:33:19 -0700" duration="21.29455310106277" durationUnit="min"/>
  <WorkoutEvent type="HKWorkoutEventTypeSegment" date="2021-06-18 05:45:32 -0700" duration="13.6915263513724" durationUnit="min"/>
  <WorkoutEvent type="HKWorkoutEventTypeSegment" date="2021-06-18 07:20:40 -0700" duration="11.98405149181684" durationUnit="min"/>
  <WorkoutEvent type="HKWorkoutEventTypeSegment" date="2021-06-18 07:28:41 -0700" duration="8.060033742586771" durationUnit="min"/>
  <WorkoutStatistics type="HKQuantityTypeIdentifierActiveEnergyBurned" startDate="2021-06-18 05:33:19 -0700" endDate="2021-06-18 07:36:49 -0700" sum="920.929" unit="Cal"/>
  <WorkoutStatistics type="HKQuantityTypeIdentifierDistanceWalkingRunning" startDate="2021-06-18 05:33:19 -0700" endDate="2021-06-18 07:36:49 -0700" sum="6.45289" unit="mi"/>
  <WorkoutStatistics type="HKQuantityTypeIdentifierBasalEnergyBurned" startDate="2021-06-18 05:33:19 -0700" endDate="2021-06-18 07:36:49 -0700" sum="338.297" unit="Cal"/>
  <WorkoutRoute sourceName="Mikian’s Apple Watch" sourceVersion="7.3.3" creationDate="2021-06-18 07:36:58 -0700" startDate="2021-06-18 05:33:19 -0700" endDate="2021-06-18 07:36:48 -0700">
   <MetadataEntry key="HKMetadataKeySyncVersion" value="2"/>
   <MetadataEntry key="HKMetadataKeySyncIdentifier" value="D1344CCA-5D84-49CE-99E7-8393A36BA4FE"/>
   <FileReference path="/workout-routes/route_2021-06-18_7.36am.gpx"/>
  </WorkoutRoute>
  <MetadataEntry key="HKIndoorWorkout" value="0"/>
  <MetadataEntry key="HKAverageMETs" value="4.85252 kcal/hr·kg"/>
  <MetadataEntry key="HKWeatherTemperature" value="91.4 degF"/>
  <MetadataEntry key="HKWeatherHumidity" value="1500 %"/>
  <MetadataEntry key="HKTimeZone" value="America/Los_Angeles"/>
  <MetadataEntry key="HKElevationAscended" value="5348 cm"/>
 </Workout>
```

#### MetadataEntry
These are some of the most common values for Workout MetadataEntry
```
HKIndoorWorkout
HKAverageMETs
HKWeatherTemperature
HKWeatherHumidity
HKTimeZone
HKElevationAscended
```

#### WorkoutRoute
WorkoutRoute will point to the gpx file with the route taken for a outdoor walk/run in the workout-routes folder

#### WorkoutStatistics
Workout Statistics provide info for calories burned and distance walked/ran
```
HKQuantityTypeIdentifierActiveEnergyBurned
HKQuantityTypeIdentifierDistanceWalkingRunning
HKQuantityTypeIdentifierBasalEnergyBurned
```

#### WorkoutEvents
[WorkoutEvents](https://developer.apple.com/documentation/healthkit/hkworkouteventtype) are not needed for my usecase so I have chosen to not ingest them. They note info about segments, laps, pausing, markers, ect

### Apple Health Kit Developer Notes
#### AHK memory usage
Apple HealthKit data ingestion complete in 28.92 seconds (1335.04 MB)

#### export.xml parsing (DTD and vertical tab \x0b)
The export.xml file has some Document Type Definition text at the beginning of the file. This makes the ET.fromstring() parse fail. We need to remove these lines from the string before parsing. There are several ways to do this. 

One option is to just skip the first 213 lines
```python
with open(apple_health_export_xml_file, 'r') as f:
    for _ in range(213):
        next(f)
    xml_string = f.read()
```

Another option is to use a regex to find the start and end of the DTD section and remove that section.

Credit to [@eotles](https://github.com/eotles/HealthKit-Analysis/blob/main/apple_health_xml_convert.py) for this much better implementation 

```python
with open(apple_health_export_xml_file, 'r') as f:
    xml_string = f.read()

    start_strip = re.search('<!DOCTYPE', xml_string).span()[0]
    end_strip = re.search(']>', xml_string).span()[1]
    xml_string = xml_string[:start_strip] + xml_string[end_strip:]
```

Other developers have found examples of vertical tabs (\x0b) in the xml string that prevent parsing. This may only be an issue in earlier versions of Apple Health Kit export. I have not seen any in HealthKit Export Version: 12. Regardless, we filter it out.

```python
xml_string.replace("\x0b", "")
```

#### export_cda.xml
export_cda follows [Clinical Document Architecture](https://en.wikipedia.org/wiki/Clinical_Document_Architecture) formatting.
I believe it contains a strict subset of information that is in export.xml. It doesnt look like it contains any of the workout/apple domain information. 

This is probably a better source for creating tables like heart rate and body weight and the like. Other exports are probably likely to follow this structure. 

I don't have a usecase for why I should develop an import function for this now instead of just using the export.xml so I will stick with just using export.xml for now

#### Unintended capture of metadata
When getting the MetadataEntry for humidity, temperature,etcfor a workout. The query also picks up metadata inside of the WorkoutRoute xml object. I don't care about storing/parsing these but they come along for the ride until its fixed.
``` 
   <MetadataEntry key="HKMetadataKeySyncVersion" value="2"/>
   <MetadataEntry key="HKMetadataKeySyncIdentifier" value="D1344CCA-5D84-49CE-99E7-8393A36BA4FE"/>
```

### Data not collected
#### Data inside records
There are some records like heart rate variability where individual recordings are included in the XML object. I don't need the individual records, so we do not record them.

#### ActivitySummary
I do not need ActivitySummary data so there is no function parsing it
```xml
 <ActivitySummary dateComponents="2021-06-15" activeEnergyBurned="0" activeEnergyBurnedGoal="0" activeEnergyBurnedUnit="Cal" appleMoveTime="0" appleMoveTimeGoal="0" appleExerciseTime="0" appleExerciseTimeGoal="30" appleStandHours="0" appleStandHoursGoal="12"/>
```

#### Data not present
Some data was defined in the DTD that was not found in the xml
- Correlation
- ClinicalRecord
- Audiogram
- SensitivityPoint
- VisionPrescription
- RightEye
- LeftEye