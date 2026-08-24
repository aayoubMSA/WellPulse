# POWDER profile/API create probe

- Checked UTC: 2026-08-24T17:26:21Z
- GitHub SHA: 52f2a189e7009a206b91dcdddc43ed64b2986ddc
- Resource action attempted: **NONE**
- Token content recorded: **NO**

## profile get help
```text
[1m                                                                                [0m
[1m [0m[1mUsage: [0m[1mportal-cli profile get [OPTIONS][0m[1m                                       [0m[1m [0m
[1m                                                                                [0m
 Retrieve a specific profile                                                    
                                                                                
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m *  [1m-[0m[1m-profile[0m[1m-id[0m        [1mTEXT[0m  The target experiment ID. [2m[required][0m            [2m│[0m
[2m│[0m    [1m-[0m[1m-help[0m              [1m    [0m  Show this message and exit.                     [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m

```

## experiment create help
```text
[1m                                                                                [0m
[1m [0m[1mUsage: [0m[1mportal-cli experiment create [OPTIONS][0m[1m                                 [0m[1m [0m
[1m                                                                                [0m
 Create a cloudlab experiment.                                                  
                                                                                
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m *  [1m-[0m[1m-name[0m                   [1mTEXT                  [0m  A human readable name    [2m│[0m
[2m│[0m                                                     for the experiment       [2m│[0m
[2m│[0m                                                     [2m[required]              [0m [2m│[0m
[2m│[0m *  [1m-[0m[1m-project[0m                [1mTEXT                  [0m  The project the          [2m│[0m
[2m│[0m                                                     experiment is            [2m│[0m
[2m│[0m                                                     instantiated in.         [2m│[0m
[2m│[0m                                                     [2m[required]              [0m [2m│[0m
[2m│[0m *  [1m-[0m[1m-profile[0m[1m-name[0m           [1mTEXT                  [0m  The name of the profile. [2m│[0m
[2m│[0m                                                     [2m[required]              [0m [2m│[0m
[2m│[0m *  [1m-[0m[1m-profile[0m[1m-project[0m        [1mTEXT                  [0m  The name of the profile  [2m│[0m
[2m│[0m                                                     project                  [2m│[0m
[2m│[0m                                                     [2m[required]              [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-group[0m                  [1mSTR                   [0m  The project subgroup the [2m│[0m
[2m│[0m                                                     experiment is            [2m│[0m
[2m│[0m                                                     instantiated in.         [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-start[0m[1m-at[0m               [1;2m[[0m[1m%Y-%m-%dT%H:%M:%S%z[0m[1;2m|[0m[1m%[0m  Schedule experiment to   [2m│[0m
[2m│[0m                             [1mY-%m-%dT%H:%M:%S.%f%z[0m[1;2m|[0m  start at a future time   [2m│[0m
[2m│[0m                             [1m%Y-%m-%d[0m[1;2m|[0m[1m%Y-%m-%dT%H:%[0m  [2m[default: Unset]        [0m [2m│[0m
[2m│[0m                             [1mM:%S[0m[1;2m|[0m[1m%Y-%m-%d         [0m                           [2m│[0m
[2m│[0m                             [1m%H:%M:%S[0m[1;2m][0m[1m             [0m                           [2m│[0m
[2m│[0m    [1m-[0m[1m-stop[0m[1m-at[0m                [1;2m[[0m[1m%Y-%m-%dT%H:%M:%S%z[0m[1;2m|[0m[1m%[0m  Schedule experiment to   [2m│[0m
[2m│[0m                             [1mY-%m-%dT%H:%M:%S.%f%z[0m[1;2m|[0m  stop at a future time    [2m│[0m
[2m│[0m                             [1m%Y-%m-%d[0m[1;2m|[0m[1m%Y-%m-%dT%H:%[0m  [2m[default: Unset]        [0m [2m│[0m
[2m│[0m                             [1mM:%S[0m[1;2m|[0m[1m%Y-%m-%d         [0m                           [2m│[0m
[2m│[0m                             [1m%H:%M:%S[0m[1;2m][0m[1m             [0m                           [2m│[0m
[2m│[0m    [1m-[0m[1m-duration[0m               [1mINT                   [0m  Initial experiment       [2m│[0m
[2m│[0m                                                     duration in hours        [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-paramset[0m[1m-name[0m          [1mSTR                   [0m  Optional name of a       [2m│[0m
[2m│[0m                                                     parameter set to apply   [2m│[0m
[2m│[0m                                                     to the profile           [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-paramset[0m[1m-owner[0m         [1mSTR                   [0m  The owner of the         [2m│[0m
[2m│[0m                                                     parameter set            [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-bindings[0m               [1mANYOBJECT             [0m  [2m[default: Unset][0m         [2m│[0m
[2m│[0m    [1m-[0m[1m-refspec[0m                [1mSTR                   [0m  For a repository based   [2m│[0m
[2m│[0m                                                     profile, optionally      [2m│[0m
[2m│[0m                                                     specify a refspec[:hash] [2m│[0m
[2m│[0m                                                     to use instead of the    [2m│[0m
[2m│[0m                                                     HEAD of the default      [2m│[0m
[2m│[0m                                                     branch                   [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-sshpubkey[0m              [1mSTR                   [0m  Additional ssh public    [2m│[0m
[2m│[0m                                                     key for the experiment.  [2m│[0m
[2m│[0m                                                     [2m[default: Unset]        [0m [2m│[0m
[2m│[0m    [1m-[0m[1m-help[0m                   [1m                      [0m  Show this message and    [2m│[0m
[2m│[0m                                                     exit.                    [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m

```

## ExperimentCreate schema excerpt
```text
schema: ExperimentCreate
required: ['name', 'project', 'profile_name', 'profile_project']
name default= None nullable= None description= A human readable name for the experiment
project default= None nullable= None description= The project the experiment is instantiated in.
group default= None nullable= True description= The project subgroup the experiment is instantiated in.
profile_name default= None nullable= None description= The name of the profile.
profile_project default= None nullable= None description= The name of the profile project
start_at default= None nullable= True description= Schedule experiment to start at a future time
stop_at default= None nullable= True description= Schedule experiment to stop at a future time
duration default= None nullable= True description= Initial experiment duration in hours
paramset_name default= None nullable= True description= Optional name of a parameter set to apply to the profile
paramset_owner default= None nullable= True description= The owner of the parameter set
bindings default= None nullable= None description= Optional bindings to apply to the profile as a JSON object
refspec default= None nullable= None description= For a repository based profile, optionally specify a refspec[:hash] to use instead of the HEAD of the default branch
sshpubkey default= None nullable= True description= Additional ssh public key for the experiment.
```
