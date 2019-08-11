#Evaluate utility (anonymization algorithm: A2-MRLH)
python SmplProg_Anonymize/A2-MRLH.py Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv Data_Anonymize/anotraces_team001_data01_IDP.csv
python Prog_Shuffle/ShuffleIDs.py Data_Anonymize Data_Anonymize_Shuffle
python Prog_Eval/EvalUtil.py Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv Data_Anonymize/anotraces_team001_data01_IDP.csv > res_sU.txt

#Evaluate security for ID-disclosure (ID-disclosure algorithm: I1-rand, attacker's team ID: 020)
python SmplProg_IDDisclose/I1-rand.py Data/PWSCup2019_Osaka/reftraces_team001_data01_IDP.csv Data_Anonymize_Shuffle/pubtraces_team001_data01_IDP.csv Data_IDDisclose/etable_team020-001_data01_IDP.csv
python Prog_Eval/EvalSecI.py Data_Anonymize_Shuffle/ptable_team001_data01_IDP.csv Data_IDDisclose/etable_team020-001_data01_IDP.csv > res_sI.txt

#Evaluate security for trace inference (trace inference algorithm: T1-rand, attacker's team ID: 020)
python SmplProg_TraceInfer/T1-rand.py Data/PWSCup2019_Osaka/reftraces_team001_data01_IDP.csv Data_Anonymize_Shuffle/pubtraces_team001_data01_IDP.csv Data_TraceInfer/etraces_team020-001_data01_IDP.csv
python Prog_Eval/EvalSecT.py Data/PWSCup2019_Osaka/orgtraces_team001_data01_IDP.csv Data_TraceInfer/etraces_team020-001_data01_IDP.csv > res_sT.txt
