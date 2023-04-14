import subprocess
import pandas as pd

CSV_PATH = './Data/bit_data/bit_data_6_model.csv'

""" 
Run the sindy_model.py file and save the min., max. values used for normalization.
Also saves the equation output for that specific set of bit_data
"""
def main():
    # Capture and process the output
    output = subprocess.run(["python", "sindy_model.py"], capture_output=True)
    output_bytes = output.stdout
    output_str = output_bytes.decode('utf-8')
    output_rows = output_str.strip().split('\r\n')
    
    # Save output to file
    model_df = pd.DataFrame(output_rows)
    model_df.to_csv(CSV_PATH, index=False, header=False)

if __name__=="__main__":
    main()