#import tensorflow.compat.v1 as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as pt
import yfinance as yf
#tf.disable_v2_behavior()

# data = yf.download('AAPL', '2016-01-01', '2018-01-01')
# data.Close.plot()
# pt.show()


def load_tickers(tickers, start, end):
    """
    Takes in a list of tickers, a start, and an end date.
    Creates a dictionary of the tickers and their associated data and then returns that dictionary
    """
    data = dict()
    for ticker in tickers:
        data[ticker] = yf.download(ticker, start, end)
    
    return data

def load_tickers_to_pickle(tickers, destination, start=None, end=None, strict=False):
    import pickle
    data = dict()
    batch_size = 256
    counter = 0
    batch_counter = 0
    remainder = len(tickers)%batch_size
    if ((start == None) and (end == None)):
        #logic: see if tickers is divisible by batch size. if it isnt then manually put the last n elements in data
        #next, download and load to the pickle each batch of data
        if ~(remainder == 0):
            for ticker in tickers[(len(tickers)-remainder):]:
                data[ticker] = yf.download(ticker, period="max")
            try:
                path = destination.split("-")
                path[0] = path[0] + str(batch_counter)
                path = "".join(path)
                with open(path, 'wb+') as file:
                    pickle.dump(data, file)
                data.clear()
                print("Finished batch " + str(batch_counter) + " of " + str(int(len(tickers)/batch_size)))
                batch_counter += 1
            except:
                print("Error opening / dumping json data to file")
                return

        for i in range(int(len(tickers)/batch_size)):
            for ticker in tickers[counter:(counter+batch_size)]:
                data[ticker] = yf.download(ticker, period="max")
            counter += batch_size
            try:
                path = destination.split("-")
                path[0] = path[0] + str(batch_counter)
                path = "".join(path)
                with open(path, 'wb+') as file:
                    pickle.dump(data, file)
                data.clear()
                print("Finished batch " + str(batch_counter) + " of " + str(int(len(tickers)/batch_size)))
                batch_counter += 1
            except:
                print("Error opening / dumping json data to file")
                return
        return

    else:
        if ~(remainder == 0):
            for ticker in tickers[(len(tickers)-remainder):]:
                data[ticker] = yf.download(ticker, start=start, end=end)
            try:
                path = destination.split("-")
                path[0] = path[0] + str(batch_counter)
                path = "".join(path)
                with open(path, 'wb+') as file:
                    pickle.dump(data, file)
                data.clear()
                print("Finished batch " + str(batch_counter) + " of " + str(int(len(tickers)/batch_size)))
                batch_counter += 1
            except:
                print("Error opening / dumping json data to file")
                return

        
        for i in range(int(len(tickers)/batch_size)):
            for ticker in tickers[counter:(counter+batch_size)]:
                data[ticker] = yf.download(ticker, start=start, end=end)
            counter += batch_size
            try:
                path = destination.split("-")
                path[0] = path[0] + str(batch_counter)
                path = "".join(path)
                with open(path, 'wb+') as file:
                    pickle.dump(data, file)
                data.clear()
                print("Finished batch " + str(batch_counter) + " of " + str(int(len(tickers)/batch_size)))
                batch_counter += 1
            except:
                print("Error opening / dumping json data to file")
                return
    return
    
def load_tickers_from_pickle(path):
    import pickle
    try:
        with open(path, "rb") as file:
            data = pickle.load(file)
            return data
    except:
        print("There was an error reading / retrieving the data")
        return

def display_tickers(data_dict, data=None, dimension=None, figure_title="Ticker Prices", figsize=(15,8)):
    """
    Takes either a dictionary of stock prices from yfinance with the data to be plotted specified, or just 
    the dict of values from yfinance. In the latter case it will plot the closing prices vs the date by default
    Examples of use:

    def load_tickers(tickers, start, end):
        data = dict()
        for ticker in tickers:
            data[ticker] = yf.download(ticker, start, end)
    
        return data

    1. -- will print whatever data you feed into it from the list represented by "close" in this case
    data = load_tickers(['AAPL', 'SPY', 'MSFT'], '2016-01-01', '2018-01-01')
    close = []
    for i in data:
        close.append(data[i].Close)
    display_tickers(data, close)

    2. -- will print close price by default
    data = load_tickers(['AAPL', 'SPY', 'MSFT'], '2016-01-01', '2018-01-01')
    display_tickers(data)
    """
    if (dimension == None):
        dimension = (1,len(data_dict))

    if (data == None):
        try:
            fig, axs = pt.subplots(dimension[0], dimension[1], figsize=figsize)
            figure_title = "Ticker Close Prices" if figure_title == "Ticker Prices" else figure_title
            fig.suptitle(figure_title)
            counter=0
            for key in data_dict:
                axs[counter].plot(data_dict[key].Close)
                axs[counter].set_title(key)
                counter += 1
            pt.show()
            return
        except:
            print("No data parameter specified. Include a list of values to be plotted and the dictionary they are contained in.")
            print("Also, please incluse at least two tickers")
            return

    fig, axs = pt.subplots(dimension[0], dimension[1], figsize=figsize)
    fig.suptitle(figure_title)
    counter=0
    for key in data_dict:
        axs[counter].plot(data[counter])
        axs[counter].set_title(key)
        counter += 1
    pt.show()
    return

if __name__ == "__main__":
    '''
    load_tickers_to_pickle(['SDRL','AA','INO','AXP','VZ','SPWH','BA','SABR','PEP','CAT','JPM','CVX','APYX','KO','DIS','AFMD','XOM','GE','HPQ','FC','HD','IBM','GO','JNJ','PSNL','MCD','RPD','PRVL','MRK','BCEL','MMM','BAC','AKRO','PFE','PG','T','TRV','UTX','WMT','CSCO','INTC','MSFT','SAM','C','AIG','HON','EFC','MO','CLPR','IP','ABT','AFL','APD','GMED','AEP','RETA','HES','AON','APA','ADM','ADP','AZO','AVY','VRSK','BLL','MBIO','BK','BAX','BDX','BRK/B','BBY','HRB','BSX','ZTS','BMY','BF-B','COG','CPB','CCL','CTL','FTR','BPRN','CLF','CLX','CMS','CEIX','CL','CMA','CAG','ED','BIG','GLW','CMI','DHR','TGT','DE','D','DOV','DUK',
                            'ETN','ECL','UIHC','PKI','EMR','EOG','ETR','EFX','EQT','FDX','M','FMC','F','LNTH','NEE','BEN','HASI','PRPL','FCX','I','MYOK','TGNA','GPS','VALU','GD','GIS','CELH','GPC','GWW','HAL','HOG','LHX','PEAK','HP','HSY','HRL','CNP','HUM','ITW','IR','IPG','IFF','J','CSTE','K','KMB','KIM','KSS','KR','LM','LEG','LEN','JEF','GRC','LLY','MCFT','LB','LNC','L','LOW','ORCL','MAXR','HST','MMC','MAS','MAT','SPGI','MDT','CVS','MU','MSI','MUR','MYL','LH','THC','NEM','BFST','NKE','NI','NSC','ES','NOC','WFC','AI','HPE','NUE','OXY','OMC','OKE','QGEN','PCG','PH','PPL','JCP','COP','PHM','PNW','PBI','QTWO','XBIT','PNC','AKBA','PPG','BKR','PGR','PEG','RTN','RHI','ALTR','R','EIX','SLB','SCHW','SHW','SJM','SNA','SO','TFC','LUV','SWN','SWK','WRB','PSA','CODA','GH','SYY','TXN','TXT','TMO','KOD','TIF','TJX','GL','JCI','VNCE','UNP','UNH','UNM','MRO','X','VAR','VTR','VFC','VNO','VMC','AMRC','WRTC','GHC','WY','WHR','WMB','WEC','ADBE','AES','AMGN','AAPL','ADSK','CTAS','ESTC','CMCSA','TAP','KLAC','MKC','JWN','PCAR','MOD','COST','GKOS','GALT','SYK','TSN','AMAT','BBBY','CAH','MTZ','CERN','CINF','VIR','WLTW','HBT','DHI','FLS','ATGE','EA','EXPD','SEAS','FAST','MTB','FISV','FITB','ITRI','FHN','BF-A','AXDX','GILD','HAS','HBAN','WELL','BIIB','RRC','NBR','NE','NTRS','PAYX','PBCT','CATS','PDCO','QCOM','ESXB','ROP','ROST','VRTS','AN','CNOB','SBUX','KEY','STT','SVRA','USB','NLOK','TROW','EVER','WM','AGN','STZ','XLNX','XRAY','RESI','ZION','DNR','PBF','IVZ','INTU','MS','MCHP','CB','CHK','JBL','ORLY','CDXC','ALL','FLIR','MCRB','EQR','ATEN','DELL','BWA','VIAV','URBN','SPG','EMN','AVB','PRU','UPS','HUD','AIV','CLNC','MCK','LMT','ABC','COF','WAT','DLTR','XPO','DRI','DO','NTAP','CTXS','DVA','FII','HIG','IRM','EL','ATI','SRCL','ETFC','ANF','NOV','DGX','ROK','AMT','AMZN','AC','RL','BXP','APH','PXD','VLO','WU','CHRW','CARE','ACN','YUM','PLD','FE','VRSN','PWR','AEE','NVDA','WBT','SEE','CTSH','ISRG','CNX','RSG','EBAY','KNSA','GS','SRE','MCO','BKNG','SRRK','FFIV','AKAM','QEP','NUAN','SLM','SBSI','DVN','GOOGL','APPF','MKTX','ALRM','NFLX','A','ANTM','CME','JNPR','BLK','DTE','NDAQ','PM','CRM','MET','GCP','TPR','FLR','EW','AMP','SIC','ZBH','CBRE','NVT','MA','TRTX','GME','KMX','ICE','FIS','CMG','WYNN','AIZ','NRG','GNW','TPC','RF','TDC','MOS','LIVX','EXPE','DISCA','CF','LDOS','WYND','FSLR','EBF','DFS','TRIP','KDP','V','FARM','LC','XYL','MPC','WPX','FFWM','ACBI','NBEV','IRET','BLMN','SNDX','OSG','LGF-B','VIRT','ETSY','PRTY','CUB','CACI','LBC','DNLI','ALEC','DXC','FBK','NTB','KALA','CLXT','HALO','AMK','SND','PHR','WWD','Y','REX','VGR','BRT','CDE','CAR','PRLB','EQC','HL','HXL','HONE','NHI','PAR','LJPC','INSE','RES','RPT','STE','SFE','TCI','KN','TWIN','WMK','STXB','SI','BCML','ABMD','MEDP','ALKS','VRNS','AMSC','COLL','PVAC','ATRI','AMAG','RM','VCRA','AXAS','TWST','BMTC','BOKF','BOOM','BPOP','BRID','ARDX','PKD','BSTC','LCTX','AJX','PTVCB','NEXT','CACC','WRK','CAMP','NEWR','WK','RDNT','HALL','RDI','ORC','SIBN','CVM','TGTX','TCF','CPK','CIA','PICO','NEX','CDZI','ATH','CBTX','COKE','MGLN','VICI','SHAK','WDR','RRR','FSB','CBPX','PTGX','ACA','PFSI','CTO','BEAT','INBK','MRNA','CULP','CVBF','OYST','BLD','CVCO','ENR','CC','CABO','LBRDK','FTSI','LBRDA','TRHC','NVST','IGMS','RXN','PARR','CWT','HMTV','TIVO','ECOL','ICHR','DCO','RYI','ICD','DSSI','PBFS','FULC','MIRM','DGICA','CVA','ABBV','PPC','DJCO','GLOG','ADI','SPLK','BCC','KAMN','PSTG','COLD','ENPH','TREC','PHAS','TER','HLNE','ROSE','AIRG','ADT','NINE','GTHX','EPAC','PETQ','EVBG','INSG','POST','EML','USWS','ACRS','BHF','OSUR','RTW','AME','ESCA','BKI','HBB','TWNK','FND','AGM','FBNC','AFI','FCNCA','CCS','MR','CIVB','FIXX','LPSN','FLIC','AXGN','PFPT','ASIX','DFIN','KLDO','STRS','BNFT','RILY','NTNX','OPBK','CBL','FRPH','TRWH','MDLA','RAPT','FSTR','S','NWL','ABM','CYRX','ZIXI','FRBK','CNSL','HY','GTN','GENC','HUBS','JELD','RCKT','GIII','EVH','LOB','GSBC','BLFS','MMAC','VBTX','PFG','FNWB','VRS','FOXF','GDP','AMOT','HEI','BYND','AMED','AXSM','HIFS','ABTX','CTMX','HNRG','PE','TNET','HRTG','JCAP','INVA','HURC','CVET','STRL','AKS','VC','IDCC','MEET','LW','ITT','IIIN','EDIT','CPT','DPLO','XELA','CNS','IMGN','IMKTA','GWRS','IMMU','IHC','CTRC','MDP','INS','NYT','IONS','BOMN','KBAL','KBH','MBI','WTBA','TMDX','LCUT','MTW','BDN','RRD','LSCC','CTVA','SITC','BFC','MKL','FI','AXNX','BTU','MIDD','QLYS','MGEE','RIG','PLAY','ASH','ETNB','UIS','MGRC','TEX','MITK','MTG','DDS','MNR','USPH','TELL','MRTN','MDB','MSEX','CAC','EVI','MGPI','ALLE','IAC','NATR','JRVR','BC','FOR','XLRN','GPX','ELAN','NR','NRIM','SNV','NSSC','OFG','OFIX','GMRE','INTL','ODC','OLP','YCBD','NCR','OTTR','MXIM','PHX','PRK','CATC','PEBK','NMRK','SANM','RNST','PKOH','CTBI','PIRS','PNRG','FIZZ','PTSI','PTC','GOOG','NAV','AVCO','QDEL','LPX','RAVN','DORM','LXFR','CTB','AMPH','DTIL','JBSS','CVNA','TWOU','EEX','PDFS','LSTR','RGEN','OUT','SBCF','SEB','SGC','SJW','CRMT','IIN','ENOB','SRCE','STAA','STFC','WSFS','SYBT','SYNL','ACHC','BCOV','LCNB','CDMO','CCXI','NG','CNBKA','THFF','TISI','EBTC','TRC','HBCP','HTBI','TRNS','PCRX','PRGX','REGI','SGMO','SPSC','TESS','USM','WTRE','UTL','HMST','MSGN','VLGEA','VSEC','SMPL','WASH','GRIF','WEYS','ACRE','WRE','WSBC','CR','DLX','WOR','FMNB','DDD','ANIP','OPY','BMCH','NCSM','FTK','CLDR','BCEI','TUP','EYPT','PBYI','ITI','AQUA','FNKO','BERY','AMBA','SPRO','EHC','XGN','KAI','FLO','NAVI','RAMP','EXTN','IRMD','TKR','MLP','BGG','APLS','RCL','PING','LGND','LII','CCK','GRA','AVT','ANGO','UVE','PQG','WINA','RAD','KSU','SPNE','NC','RCKY','PSX','OSMT','FEYE','SERV','SCI','WATT','SAVE','EPAM','CFB','TEN','CASA','MTX','SCVL','IT','ALG','HR','SWI','GPRO','FCAP','AVX','CHMI','PBPB','SMHI','AEL','FL','WBC','MXL','CDNA','SVC','DHC','HRI','CLBK','LEVL','CHDN','CWEN-A','OPI','TCBK','LECO','BRG','SNR','MPB','BANF','AGE','IQV','PNTG','NVRO','BBSI','CCF','FRTA','ERI','GABC','MDLZ','RYAM','SNDR','ELS','THRM','VVI','CAL','COMM','TPIC','IIPR','BFAM','BCO','ATEX','SKY','SPXC','IRT','EB','TTD','FDEF','GPI','TERP','SAGE','BSVN','GCO','MIK','CNA','NEU','CMLS','NL','RC','CWEN','SRNE','AERI','BWB','PVBC','PKG','AUB','DSKE','GTYH','QCRH','UPLD','CHRS','CFMS','SOLY','PI','ELF','SMMF','GTY','CWK','EIDX','INCY','PDLB','PTN','SLAB','CNTY','QTS','GOSS','SRI','OSBC','RBB','NRZ','PUB','SUI','SUPN','PFNX','FRPT','SYNH','AMBC','HIIQ','EIGI','CATM','HT','RGNX','UFPT','CLNY','FNF','TMST','CPLG','BCRX','TACO','VOYA','XNCR','XEL','RGCO','LILA','LILAK','ONDK','TBK','EPRT','APAM','PEBO','KHC','TIPT','REV','MTDR','SLCA','ELVT','WSR','FG','AR','LYFT','CXP','MGTX','VAC','PCYO','HARP','NNBR','AMNB','ATLO','ARTNA','NKTR','CCNE','LKFN','MGNX','FCBC','NKSH','MPAA','SHEN','SBBX','BCOR','BDGE','GHM','CCBG','MNST','INSW','WPG','SONO','BANC','WING','ANAB','STML','BMRC','SMBC','LADR','TLYS','NOW','ALEX','UUUU','BRX','MDGL','XFOR','ALTM','ERA','OKTA','ABCB','FGBI','KURA','RMNI','PENN','TPRE','ARLO','ZUO','GBX','AVYA','MLR','HGV','PK','RVNC','MGTA','FR','PGC','KZR','ZEUS','XERS','AVRO','FRGI','VREX','IIIV','AVTR','LNG','REVG','JNCE','AZPN','CPE','DXPE','AMH','YMAB','BSGM','PLPC','IBKC','VRTV','CVTI','OVBC','SASR','GBL','SBGI','VCYT','BHB','NVEC','UNTY','CBZ','AIR','SYX','APLE','KRNY','ACNB','PWOD','BANR','KFRC','RICK','NWPX','SIX','POR','YORW','BBX','CMCO','PRSP','LNDC','WH','WHD','IDT','CASS','CVIA','KVHI','PFBI','NBIX','RUSHA','ATKR','CASI','DECK','MFIN','OCFC','FFG','PEGA','VLY','CZNC','CVLY','AIT','DHIL','KRYS','ASC','SFM','NOVT','RYTM','TPH','ADMA','AJG','YGYI','SYKE','RPAI','RTRX','GLYC','APLT','BRBR','WDAY','CSTL','LVGO','USNA','HCAT','LIVN','FCBP','ESNT','DOW','CYCN','NOVA','PROS','AKRX','UVSP','XON','NSA','NTRA','GDDY','FFIC','MMI','ALCO','SWCH','CSTR','MATX','CTRA','OVLY','BUSE','CARO','ISTR','NERV','SBBP','FTV','INSP','RUBI','PS','JYNT','UBFO','EPM','WSC','OLED','HTLF','VER','XENT','ALK','MTN','GERN','FNLC','HOLX','GPK','FDP','PROV','WLFC','CSV','ANIK','DD','PAG','CERS','PLUS','CMBM','OCN','NUS','CBAN','GWB','NWFL','HLIO','FCPT','CVCY','SPPI','RDFN','NBN','JILL','FIBK','BSRR','VCEL','PGNX','AAL','SIEB','AOBC','EEFT','LTS','FCCY','SSB','HCKT','PRIM','SLP','ASRT','ORRF','RMBS','HSKA','COLM','HOFT','SHBI','LBAI','GLPI','SENS','QADA','AHH','PDM','TSBK','UNIT','BYSI','CWST','ALOT','PSMT','MBWM','SIGA','ATEC','RVSB','RMBI','SAH','RHP','CHH','IGT','CFFI','ATSG','WCC','CNXN','WMC','SCS','SAFE','NHC','HFWA','ZS','RLH','RMTI','NVAX','CLAR','CRAI','ALBO','MCBC','BAND','AXTI','OSPN','SGH','SRG','PFBC','MFNC','SP','CSGP','TREX','STL','FNHC','ECOR','GCBC','OPRX','TWI','AXL','TCS','EGBN','PFIS','ALX','HTBK','TEAM','RBCAA','ORGO','BOCH','CFX','EVBN','CSLT','UCFC','APY','MCB','FET','MRC','UA','QUAD','QUOT','ATUS','MORN','GDEN','CFFN','AGO','EXTR','RUBY','REPH','CRNX','VHC','CCB','RTIX','EVRI','HZNP','EVR','HWBK','WOW','CNNE','FISI','SFIX','SAIL','EGOV','AGLE','EOLS','PTE','PMBC','SFST','IMMR','MOFG','HSTM','OMF','VEEV','DNOW','KTOS','PLUG','CLCT','BGCP','ATRA','LIND','BRKR','TSC','UNB','ACER','AGEN','WTI','ACOR','ABG','STAY','DVAX','RBNC','EGAN','FORM','HHC','H','BNED','EE','BLDR','WD','WWE','TXMD','CNDT','GAIA','IRTC','DZSI','ENTG','ENV','FBMS','EFSC','MFSF','FSBW','APPS','FLNT','DLA','NXRT','ARL','RIGL','APPN','LMNX','NYMT','EXEL','LXRX','COTY','FDBC','CHCT','BHLB','ARNA','INVH','RARX','LAUR','ZYXI','LTHM','WVE','CUE','ALDX','EXAS','USLM','CCOI','OSTK','ZAYO','ESPR','NSTG','FLWS','XXII','TTGT','PYPL','FTDR','RCM','IRWD','ENVA','RP','CPRX','SLCT','AXTA','EME','SGEN','IAA','NTLA','TZOO','ZIOP','WPC','XHR','AAXN','UBX','WNEB','CORT','KDMN','WHG','IPGP','AWI','QNST','PKBK','CUTR','CSOD','NGS','MEIP','MNKD','HCI','NLSN','SBT','EQBK','VYGR','DXCM','CTSO','BCBP','SBRA','SVMK','CDXS','PLAN','ALLO','PODD','CTT','CYTK','LCI','NNI','SAIA','KNSL','PRTK','WLK','RUSHB','ESGR','GTS','ACTG','NPTN','GTT','PRGO','AHT','LMAT','GOOD','TOWN','PRSC','ALNY','CADE','HCC','NESR','TPX','PRAH','MRLN','ARMK','HLT','GBLI','SALT','FRME','CONN','FLXN','EGRX','WIFI','CMPR','PRI','RMR','CMCT','KRO','TDOC','MCHX','OAS','HTH','CDW','HDS','TCMD','UCTT','TBPH','CTRE','ASGN','AKTS','KTB','LRN','KIN','CPS','CDAY','ACHN','BXS','CBSH','TRMK','PRTH','UMBF','MTEM','GCI','ERIE','WABC','TCBI','PACW','CBNK','MNTA','CNO','TLRA','ETRN','REG','GRTS','IBP','REPL','FGEN','ALLK','FLDM','ETH','CHNG','ADPT','MORF','BBIO','CIEN','GSIT','WBA','DPZ','MAR','TRUP','CNCE','EAT','CDNS','NGVT','CRS','CY','JOE','TYL','UHS','HURN','AGCO','SWKS','CRC','ATVI','EBIX','HFC','JKHY','KPTI','PDLI','AFIN','PRGS','CNST','RGLD','SNPS','PTEN','SCHN','RS','ACIA','ADTN','HSIC','ANSS','FDS','AMG','TTWO','JLL','MSTR','SBAC','ON','ORA','MDRX','CRL','TCFC','BWXT','BLKB','OIS','BG','WLL','XRX','HPR','CE','KBR','SXC','HII','GT','PNM','TWTR','CFG','YEXT','CFR','FCFS','SUM','JHG','PB','EVFM','EVC','MRKR','LYV','TOCA','WMS','OEC','CVGI','AMSWA','COO','MAN','OII','VHI','VSH','TECD','ATR','RMD','LAZ','MTD','VBIV','ARVN','BMRN','SPWR','BECN','VPG','MNOV','WAL','AMPY','PINC','TAST','GTES','MNLO','SHO','GOLF','FOXA','VIAC','FOX','PLMR','TPTX','CHD','DRE','VIACA','FRT','MDU','MGM','ODP','METC','TOL','AMWD','TBBK','EV','FOSL','SSTI','JBHT','LRCX','MHK','PNR','AAWW','SEIC','VRTX','CUBE','CREE','MLVF','MAC','NYCB','RNR','WMGI','SIRI','MLM','LTRPA','RYN','LPT','BHVN','JOUT','SCCO','BXC','GWGH','LGIH','FNCB','AAOI','ACGL','DISH','FB','ALXN','RE','AMTD','NLY','ICFI','KNL','FLOW','CCI','CLR','PBIP','RRBI','AAP','ILMN','STRO','ADS','SEM','USX','DLB','CHRA','DOC','REXR','EPC','MRVL','SAIC','GRMN','ANAT','XEC','REAL','KRTX','TPCO','HLF','AXS','DLR','LVS','DISCK','LYB','ULH','AVGO','QRTEA','BXG','HTZ','FLT','SCU','CXO','LULU','EXLS','AWK','CUBI','GM','DG','CIT','LEGH','KMI','RNG','ARAY','KALV','HCA','NWSA','ORI','GLDD','OCUL','LOCO','VEC','OFLX','WTM','CORE','TDS','AEO','ARD','NXST','CTRN','EXC','HSC','AM','DBI','LBRT','TFSL','PD','CLGX','MYGN','CRNC','AVLR','DEA','WTR','FCN','UDR','EGLE','URGN','ADES','SWAV','SD','LAMR','SLG','HUN','AX','UFS','WSM','ARES','LITE','STLD','VAPO','AROC','NMIH','OSK','JAZZ','AGR','STAR','BRO','GPMT','CARS','VKTX','ATRC','OI','BOX','PRDO','HBI','BR','HRC','RDN','CHS','CYH','MNRL','ROLL','EAF','DT','HOOK','GPRE','MPX','DENN','GNLN','VNDA','STOR','INGN','VSTO','USCR','ISBC','WSBF','ILPT','ULTA','LPG','ADNT','SBOW','KREF','MUSA','FN','TPB','BL','TCRR','UMH','NCBS','EYE','ACCO','NBL','LE','CARG','GRUB','KIDS','AOS','BKD','FF','NVEE','SSP','MRTX','AMC','SONA','OPRT','AGS','SLDB','FMBH','PGRE','HEES','PLSE','INFN','ELY','AKCA','GFN','NTGN','BPMC','LOVE','TDG','CBOE','KLXE','NGM','SILK','AGX','PRNB','UEC','YELP','SPKE','GES','RH','CERC','KRUS','INST','CORR','PSN','CDK','MWA','CKPT','BPR','COWN','ARCH','ADSW','BRP','MGY','LOGC','GTLS','LEAF','FIVE','INWK','KRG','IESC','JAX','FOLD','FTNT','AYR','AMEH','DEI','FATE','DOX','NCLH','SPR','BDSI','RCUS','CSFL','PEN','IPHS','WLDN','HA','III','OSW','ZAGG','CELC','CLNE','OMER','OC','LLNW','RNET','AIMC','YUMC','GEN','NCMI','CBMG','ARNC','DHX','RUN','WLH','COOP','PANW','ATHX','CSX','CZR','TEUM','VG','TRN','UFI','SBH','ESRT','BURL','RMAX','GRBK','MNSB','ARE','PACB','GLUU','GLRE','WTRH','CLFD','CNK','CAI','REI','WAAS','CHGG','COUP','TNAV','EROS','ESSA','PRO','CHAP','KAR','LFVN','BATRA','BATRK','LSXMA','LSXMK','TSLA','ECHO','CVI','PZN','SSNC','FWONA','FWONK','G','SAMG','ROIC','ZYNE','EVRG','TRS','KW','PGNY','HABT','TRGP','TITN','MNK','NWS','SSYS','AMAL','CWH','FIVN','EBSB','SITE','TMHC','FFNW','TMUS','CDEV','ARWR','MMS','NFBK','MTCH','SQ','IRDM','CONE','SMBK','DAN','WGO','SATS','HMHC','TNDM','PLNT','AIMT','ST','ZGNX','ERII','MG','LOPE','AMRS','RRTS','NODK','APOG','RST','MEC','ASPS','SPFI','CRTX','ACRX','NXTC','AXLA','GCAP','AIN','TBNK','ATO','BOH','B','BKH','LPLA','MTRN','TRTN','JBGS','CBT','CSL','BKU','CHE','CBB','IPHI','CMC','CTS','CW','DBD','PEB','DCI','DY','GNRC','ESE','CLDT','FSS','LEA','FCF','UNFI','JACK','TRNO','GATX','AJRD','CALX','GGG','HAE','POL','HE','CRMD','MTH','CHTR','HMN','UBA','HUBB','OPTN','IDA','IEX','INT','AXE','KMT','ESTE','LZB','SR','LDL','PLOW','MDC','EXPR','ALE','HPP','MLI','NFG','GDOT','NPK','NJR','OGE','OLN','PRMW','OMI','GNMK','DOOR','OXM','PKE','TDW','AFG','PVH','THR','PCH','RJF','RLI','ROL','NGHC','SJI','COR','TRXC','SWX','NDLS','SMP','UNVR','CSWI','FIT','PJT','SXI','BAH','QRVO','BTAI','AL','SF','MSG','RGR','THO','ZG','FMAO','TR','TTC','TG','UGI','UNF','UNT','TYME','SXT','VRA','UHT','UVV','TALO','AVA','WRI','BE','WST','GNC','WWW','CBRL','HNI','KELYA','SC','MLHR','SON','GNTY','ESI','AAON','VRNT','ARCB','MESA','AVD','TVTY','AAN','ATNI','AZZ','BELFB','ASMB','MCBS','FREQ','BHE','APRE','BIO','KNX','VIE','BKE','CNR','STAG','CTLT','MYRG','BMI','SYF','BRC','INN','CATO','CAKE','AAT','CASY','CHEF','CATY','CBU','CDR','CENTA','CGNX','CHCO','CLH','CRK','RLJ','CMTL','CNMD','CMD','COHU','COLB','BH','GNE','CRUS','CRVL','ASNA','DGII','FRC','DIOD','DNKN','RDUS','LCII','WEN','EGP','ENZ','EZPW','EXPO','FNB','FELE','FFBC','FBP','FICO','FMBI','FUL','FULT','GBCI','GVA','TORC','GNTX','HVT','HWC','HCSG','HELE','HNGR','HMSY','HTLD','HWKN','ICUI','MODN','IDXX','TILE','CBAY','DIN','IIVI','INDB','BLUE','AEGN','GFF','IVC','IPAR','JJSF','KEX','VIVO','ANET','LANC','LAWS','LNN','ADMS','LXU','CMRX','PRA','MEI','MMSI','MSA','MNRO','MOG-A','MCS','MCY','HFFG','BWFG','MTRX','MTSC','MYE','NBTB','NDSN','NEOG','NNN','NVR','NWN','EVTC','ODFL','RLGT','CUZ','PEI','PDCE','AGYS','SFBS','PLXS','CRCM','POWL','PSB','KWR','NXGN','RBC','REGN','RGS','OFC','UEIC','ROG','DLTH','RPM','SAFM','SCHL','SCL','SMG','SENEA','REZI','SFNC','BXMT','SIGI','CMO','CRD-A','LASR','STC','ELOX','SIVB','SMTC','LEN-B','PII','BLBD',
                            'SPAR','PCTY','STBA','AWR','MRNS','TNC','HQY','TMP','LMNR','TECH','TFX','ADVM','SGMS','BLX','TRMB','TRST','TTI','UBSI','ARW','UFCS','PAHC','KMPR','HEI-A','PTCT','VST','VMI','VICR','DX','TTEK','WTS','WBS','WDFC','WERN','FRBA','WAFD','JW-A','WIRE','WRLD','WSO','ZBRA','SKT','WTTR','SIG','AYX','LTC','OHI','TCO',
                            'PUMP','LFUS','SM','CHUY','CKH','BFIN','CRY','APTS','AKR','HOME','RGA','PZZA','GEF','BYD','MCRI','MOV','BFS','OPK','MHO','ROCK','AVID','VSLR','UBER','CRBP','UFPI','VRRM','LXP','ONTO','FFIN','FWRD','HAIN','MAA','TWLO','SHOO','TSCO','PLT','MED','CPRT','DAKT','ALB','IDEX','TBI','ESQ','DSPG','BPFH','MINI','DAR','SCSC','GEF-B','FHB','EXP','AMRX','HIW','CALM','SSD','ESS','GEO','MATW','CLI','TK','O','IMAX','NSIT','PYX','NWBI','VECO','ANDE','SLGN','BRKS','ACIW','RCII','NATI','LGF-A','IART','IBOC','HLIT','BXRX','WAB',
                            'RWT','LSI','NAT','POOL','MD','CENX','AEIS','PHAT','CABA','CSGS','VMW','TTEC','DCOM','LORL','THG','ROAD','GEOS','SWM','HOPE','HAFC','ANH','ATRS','HUBG','STRA','MASI','HIBB','CHMA','AMSF','MFA','TGI','HLX','WTFC','ADC','FORR','VSAT','LAD','PLCE','BJRI','OLLI','NSP','KRC','GLIBA','SKYW','SPTN','UMPQ','CXW','OSIS','OZK','GPOR','NGVC','JBLU','FIX','DS','FARO','EPR','AMCX','PETS','POWI','BJ','HI','BV','DRQ','SFL','AMD','TBIO','FTSV','URI','KOS','TCDA','MKSI','INGR','AT','SRDX','MANH','HBMD','BRKL','GOGO','MRCY','WDC','STIM','BIOS','CPA','XAN','BRY','HSII','DHT','FOCS','HZO','TENB','DAL','KFY','XOG','SKX','ZNGA','SNBR','UAL','CNC','CRI','ARR','EPAY','CIM','FLMN','EWBC','JCOM','TGH','RFL','STMP','UCBI','ECPG','CIR','TNK','ATNX','RECN','SB','LPI','CVLT','IVR','ACM','AVAV','PMT','STWD','GNK','TWO','GHL','ARI','BGSF','NTUS','NTCT','PRFT','SYNA','XPER','STNG','UTHR','TDY','DKS','FVCB','MANT','CMRE','ENDP','CCMP','OMCL','ITGR','PNFP','TTMI','NOG','MITT','GPN','PACD','NTGR','RUTH','BHR','CIO','APTV','SNX','ALGN','CVGW','CPRI','FSP','AYI','CCRN','AMN','CPSI','LQDA','LKQ','BSIG','SCOR','SNCR','NUVA','IMXI','CMP','ENS','CEVA','ASB','SAFT','RRGB','NPO','SPOK','PCSB','PFS','PRAA','WW','ADRO','EQIX','MOH','PIPR','BGS','INFO','UPWK','SBNY','VRTU','ACC','FPI','TXRH','MRSN','EXR','MPW','DRH','NP','MPWR','BDC','W','RVI','HAYN','LQDT','HOMB','UE','AMTB','NWE','PBH','KOP','WEX','LHCG','ZUMZ','THS','EBS','IRBT','CROX','UAA','EHTH','ALGT','KALU','LOGM','IBKR','EIG','LL','ENSG','UHAL','MSCI','APEI','JBT','NX','IPI','FAF','ENTA','EXPI','CLW','KRA','FBHS','INOV','ARGO','TCX','NVTA','CALA','DOMO','NRC','SRT','ZEN','TSE','PCB','PAYS','SONM','MOBL','PHUN','SIEN','CPF','IBCP','WNC','AROW','YRCW','PAYC','FBC','GBT','FOE','ONB','ACLS','BSET','MTOR','CIX','CISN','BY','ROKU','PLAB','DCPH','ETM','OMN','LEE','MIC','KEM','MDCA','CI','CETV','CWCO','TUSK','IOSP','ECOM','IOTS','GLNG','GORO','ALSN','AGNC','TLRD','AOSL','GRPN','OBNK','MTSI','CLVS','CCO','STOK','CDLX','COHR','FBM','HLI','MSBI','ABEO','MSON','BZH','LNT','HCCI','WETF','CSII','HRTX','GLT','ICPT','ASTE','PGTI','PTLA','YETI','EPZM','ACAD','KEYS','AVNS','IBTX','KE','PEGI','SRPT','NATH','CECE','BOOT','CHMG','CASH','IOVA','TRU','ITIC','CENT','MLAB','GNL','BREW','UI','DMRC','DK','ORBC','UTMD','ADUS','TREE','FRAF','RBBN','PRTA','SOI','LAND','NWLI','FPRX','SGRY','PFGC','SPB','FBIZ','EVLO','SPOT','SWTX','STSA','ALRS','CURO','EQH','MBIN','FSCT','TH','VVV','EIGR','DRNA','GRTX','CNTG','SGA','ARA','HTA','OGS','INSM','RARE','MBUU','AMKR','TRUE','SYBX','EGHT','Z','MC','RLGY','OPB','FLXS','HBNC','PATK','PPBI','SHSP','CARA','ITCI','LIN','MLND','MJCO','SMAR','DOCU','GWRE','ATRO','DERM','SSTK','NBHC','MBII','SRC','GDI','BBCP','OCX','EVOP','MSM','FANG','DBX','NVCR','ODT','NEO','MVBF','QTRX','VRCA','VRAY','TROX','AVXL','OOMA','BCPC','GSHD','GMS','USFD','AGIO','SCWX','SYRS','ALLY'], "../data2/russel3000/-_data.pickle")
    '''
    data = load_tickers_from_pickle("../data2/russel3000/2_data.pickle")
    print(data)
