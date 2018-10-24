def retrieve_classification(page_data):
    Numbers_data      = page_data.find_all("th", class_="msr_col2")
    Drivers_data      = page_data.find_all("td", class_="msr_col3")
    Teams_data        = page_data.find_all("td", class_="msr_col4")
    Times_data        = page_data.find_all("td", class_="msr_col5")
    Laps_data         = page_data.find_all("td", class_="msr_col6")
    GridPos_data      = page_data.find_all("td", class_="msr_col8")
    Points_data       = page_data.find_all("td", class_="msr_col9")

    Positions         = []
    Numbers           = []
    Drivers           = []
    Teams             = []
    Times             = []
    Laps              = []
    GridPos           = []
    Points            = []
    
    for i in range(len(Numbers_data)-1):
        Positions.append(str(i))
        Numbers.append(str(Numbers_data[i+1].get_text()))
        Drivers.append(str(Drivers_data[i].get_text()))
        Teams.append(str(Teams_data[i].get_text()))
        Times.append(str(Times_data[i].get_text()))
        Laps.append(str(Laps_data[i].get_text()))
        GridPos.append(str(GridPos_data[i].get_text()))
        Points.append(str(Points_data[i].get_text()))
    return Positions, Numbers, Drivers, Teams, Times, Laps, GridPos, Points

def retrieve_GPs_list(page_data):
    GPs_data  = page_data.find_all("a")
    GPs_list  = []
    for data in GPs_data:
        dummy = data.get_text()
        if (len(dummy)>0) and (dummy[-6:] == "result"):
             GPs_list.append(dummy[:-13])
    return GPs_list

def retrieve_years_list(page_data):
    year_data = page_data.find_all("option")
    years_list = []
    for data in year_data:
        dummy = data.get_text().split()
        if dummy[-1] == "Standings":
            years_list.append(dummy[0])
    return years_list

