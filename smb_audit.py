import sys
import os
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
from datetime import datetime
import feather
import math
import glob
import logging

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def extract_epoch(seq):
    seq_type= type(seq)
    return int(seq_type().join(filter(seq_type.isdigit, seq)))

def convert_time(epoch_time):
    return datetime.fromtimestamp(extract_epoch(epoch_time))

def show_ftr_details(df):
    logging.info('Most recent time of dataset: ' + str(df.local_time.max()))
    logging.info('Oldest time of dataset: ' + str(df.local_time.min()))
    logging.info('Time between start and end of dataset: ' + str(df.local_time.max() - df.local_time.min()))
    logging.info("=====================================================") 
    

def parse_audit(source_directory, output_file):
    pd.set_option('display.max_rows', None)
    col_names = ["col0", "col1", "col2", "col3", "result", "col5", "user", "col7", "smb_operation_type", "utc_time", "local_time", "col11", "share", "path", "col14", "col15", "col16", "col17"]
    small_dfs = [] 

    all_files = glob.glob(os.path.join(source_directory, "audit.*.log"))
    total_size = 0

    for file in all_files:
        total_size += os.path.getsize(file)
    logging.info(all_files)
    df_from_each_file = (pd.read_csv(f, sep='|', names=col_names, index_col=False, low_memory=False, parse_dates=['local_time'], date_parser=convert_time, usecols=[4, 6, 8, 10, 12, 13]) for f in all_files)

    concatenated_df  = pd.concat(df_from_each_file, copy=False)
    #concatenated_df.info()
    #logging.info(concatenated_df.memory_usage(deep=True) / 1e6)

    concatenated_df.smb_operation_type  = concatenated_df.smb_operation_type.astype('category')
    concatenated_df.info()
    logging.info(concatenated_df.memory_usage(deep=True) / 1e6)


    logging.info('Creating feather file at: ' + str(output_file) + ".ftr")
    concatenated_df.reset_index().to_feather(output_file + ".ftr")
    #if (make_csv):
    #    csv_file_name = output_file + ".csv"
    #    logging.info('Creating output file at: ' + csv_file_name)
    #    concatenated_df.reset_index().to_csv(csv_file_name, index = False, compression = 'gzip')
    #    os.rename(csv_file_name, csv_file_name + ".gz")
                
    ftr_size = os.path.getsize(output_file + ".ftr")
    logging.info("Completed parsing " + str(convert_size(total_size)) + " to " + str(convert_size(ftr_size)))
    logging.info("=====================================================")
    logging.info('Most recent time of dataset: ' + str(concatenated_df.local_time.max()))
    logging.info('Oldest time of dataset: ' + str(concatenated_df.local_time.min()))
    logging.info('Time between start and end of dataset: ' + str(concatenated_df.local_time.max() - concatenated_df.local_time.min()))
    logging.info("=====================================================")  

def summarize_audit(ftr_file, time_interval):
    df = pd.read_feather(ftr_file)
    logging.info('Loading FTR file at: ' + str(ftr_file))
    logging.info("=====================================================")
    show_ftr_details(df)
    logging.info('Totals per SMB operation type for this dataset:\n' + str(df['smb_operation_type'].value_counts()))
    logging.info("=====================================================")
    logging.info('Top 10 users for this dataset:\n' + str(df['user'].value_counts().nlargest(10)))
    logging.info("=====================================================")
    logging.info('Top 10 shares for this dataset:\n' + str(df['share'].value_counts().nlargest(10)))
    logging.info("=====================================================")
    logging.info('Top 10 paths for this dataset:\n' + str(df['path'].value_counts().nlargest(10)))
    logging.info("=====================================================")
    #logging.info(str(df.groupby([df.local_time.dt.floor(time_interval), 'smb_operation_type']).size()))
    
    plt.rc('legend',fontsize=6)
    #df.groupby([df.local_time.dt.floor('60min'), 'smb_operation_type']).size().plot()
    #df.groupby([df.local_time.dt.floor(time_interval), 'smb_operation_type']).size().unstack().plot(colormap='nipy_spectral').legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
    df.groupby([df.local_time.dt.floor(time_interval), 'smb_operation_type']).size().unstack().plot(colormap='nipy_spectral', x_compat=True).legend(loc='best')
    #df.groupby([df.local_time.dt.floor(time_interval), 'smb_operation_type']).size().unstack().plot(colormap='nipy_spectral', x_compat=True).legend(loc='best')
    plt.show()
    
def search_audit(ftr_file, search_field, search_string, show_smb_ops):
    df = pd.read_feather(ftr_file)
    logging.info('Loading FTR file at: ' + str(ftr_file))
    logging.info("=====================================================")
    show_ftr_details(df)
    #logging.info(df[df[arguments.search_field].str.contains(arguments.search_string)].to_string())
    search_results = df[(df[search_field].str.contains(search_string)) & (df['smb_operation_type'].isin(show_smb_ops))].to_string()
    logging.info(search_results)

def smb_audit(args):
    try:
        if (args.is_debug):
            logging.debug("Usage:\n{0}\n".format(" ".join([x for x in sys.argv])))
            logging.debug("")
            logging.debug("All settings used:")
            for k,v in sorted(vars(args).items()):
                logging.debug("{0}: {1}".format(k,v))
        
        if (args.function == 'Parse'):
            parse_audit(args.source_directory, args.output_file)
        
        if (args.function == "Summarize"):
            summarize_audit(args.ftr_file, args.time_interval)
   
        if (args.function == "Search"): 
            #Create List of SMB Operations to show in Search    
            show_smb_ops = []
            if (not args.ACEChanged): 
                show_smb_ops.append('op=ACEChanged')
            if (not args.ACLAdded):
                show_smb_ops.append('op=ACLAdded')
            if (not args.ACLDeleted):
                show_smb_ops.append('op=ACLDeleted')   
            if (not args.AclDenied):
                show_smb_ops.append('op=AclDenied')        
            if (not args.chown):
                show_smb_ops.append('op=chown')           
            if (not args.create):
                show_smb_ops.append('op=create')            
            if (not args.createDenied):
                show_smb_ops.append('op=createDenied')
            if (not args.delete):
                show_smb_ops.append('op=delete')
            if (not args.deleteDenied):
                show_smb_ops.append('op=deleteDenied')
            if (not args.move):
                show_smb_ops.append('op=move')
            if (not args.open):
                show_smb_ops.append('op=open')
            if (not args.OpenDenied):
                show_smb_ops.append('op=OpenDenied')
            if (not args.setattrib):
                show_smb_ops.append('op=setattrib')
            if (not args.setdacl):
                show_smb_ops.append('op=setdacl')
            if (not args.write):
                show_smb_ops.append('op=write')
            search_audit(args.ftr_file, args.search_field, args.search_string, show_smb_ops)
    except KeyboardInterrupt:
        logging.getLogger().fatal('Cancelled by user.')    
