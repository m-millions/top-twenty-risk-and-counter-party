import csv
import glob
import heapq


#def calculate_risk_loss(trades_sell, trades_buy):
def calculate_risk(trades_sell, trades_buy):
    '''
    Get for BUY SIDE and SELL SIDE for each counter party and
    calculate RISK
    TO DO: Calculate and Return Loss
    '''
    #TO DO: Finish Loss Calculation
    #loss_positions = []
    risk = ''
    risk_positions = []
    #TO DO: try this using map()
    for ts in trades_sell:
        for tb in trades_buy:
            if ts[1] == tb[1]:
                # CALCULATE if we sold securities for less than we bought them
                loss = (float(ts[4])*float(ts[5])) - (float(tb[4])*float(tb[5]))
                # CALCULATE if we have sold less securites than we bought
                if loss < 0:
                    #loss_positions.append(ts[1])
                    #loss_positions.append(ts[2])
                    risk = (int(tb[4]) - int(ts[4]))
                    if risk < tb[4] and risk > 0:
                        tbs = []
                        tbs.append(risk)
                        tbs.append(tb[2])
                        tbs.append(tb[1])
                        risk_positions.append(tbs)
                break            
    risk_positions = sorted(risk_positions)
    #TO DO: Return loss object
    #return risk_positions, loss
    return risk_positions 

def generate_stats():
    '''
    WRITE all data in CSV files; write as many files as 
    there are objects returned by the function call
    TO DO: Report Loss
    '''
    tops = process_trade_information()
    #TO DO: Include a new file to report loss calculations
    #c_files = ["top_twenty_risks.txt",
    #           "top_two_counter_parties_dollar_volume.txt",
    #           "loss_report.txt"]
    c_files = ["top_twenty_risks.txt",
               "top_two_counter_parties_dollar_volume.txt"]

    file_name = c_files[0]
    for o in tops:
        with open(file_name, 'wb') as top:
            writer = csv.writer(top, delimiter=',')
            writer.writerow(o)
        file_name = c_files[1]

def get_counter_party(f):
    '''
    Extracts Counter Party name from file name
    and returns them for processing
    '''
    cpn = ''
    for i in range(0,3): 
        cpn += f[i] 
    return cpn

def get_marks():
    '''
    Reads all Securities "Marks" into a list for 
    inclusion as part of Risk Position record
    '''
    smark = ''
    smarks = []
    with open('marks', 'rb') as m:
        reader = csv.reader(m)
        for m in reader:
            smark = m
            smarks.append(smark)
    return smarks   

def get_top_twenty_risk(risk_positions):
    '''
    CALCULATE RISK for Holdings in Securities
    '''
    srisks = []
    risk_positions = sorted(risk_positions)
    smarks = get_marks()
    #TO DO: Try this using map()
    for rp in risk_positions:
        for smark in smarks:
            if rp[2] == smark[1]:
                srisk = []
                srisk.append(rp[0])
                srisk.append(rp[1])
                srisk.append(rp[2])
                srisk.append(smark[2])
                srisks.append(srisk)
                break
    # GET TOP 20 = Asset RISK Long Positions
    t20 = heapq.nlargest(20, srisks)
    return t20

def process_trade_information():
    '''
    READ IN trade data from all files that are marked .csv
    in corresponding directory
    TO DO: Return Loss 
    '''
    cparties= []
    final_cp_volume = []
    final_trades = {}
    risk_positions = []
    top_twenty_risks = []
    trade_in = ''
    trades_buy = []
    trades_sell = []
    volume_total = ''

    for f in glob.glob("*.csv"):
        cp_name = ''
        cparties.append(f)
        # Get Counter Party name from file name
        cp_name = get_counter_party(f)
        with open(f, 'rb') as f:
            reader = csv.reader(f)
            volume_total = 0
            cp_volume =[]
            for r in reader:
                trade_in = r
                trade_volume = ''
                # Pass in all BUY trades for the 
                # counter party
                if trade_in[3].strip() == "BUY":
                    trades_buy.append(trade_in)
                # Pass in all SELL trades for the 
                # counter party
                elif trade_in[3].strip() == "SELL":
                    trades_sell.append(trade_in)
                trade_volume = float(trade_in[4]) * float(trade_in[5])
                volume_total += float(trade_volume)
            cp_volume.append(volume_total)
            cp_volume.append(cp_name)
            final_cp_volume.append(cp_volume)           
        print "   "
        print volume_total
        # stores counter party name and trading volume in dollars
        print cp_volume 
        # final list object which stores ALL counter partis 
        # and their trading volumes as lists
        print final_cp_volume        
    # Calculate top 2 Counter Parties
    top_two_counterparties = heapq.nlargest(2, final_cp_volume)
    print "   "
    print top_two_counterparties
    print "   "
    #TO DO: include loss calculation
    #risk_positions = calculate_risk_loss(trades_sell, trades_buy)   
    risk_positions = calculate_risk(trades_sell, trades_buy)
    top_twenty_risks = get_top_twenty_risk(risk_positions)
    #TO DO: Return Risk Positions
    #return top_twenty_risks, top_two_counterparties, risk_positions
    return top_twenty_risks, top_two_counterparties 

def main():
    '''
    Calls generate_stats to start processing data
    '''
    generate_stats()

if __name__ == '__main__':
    main()
