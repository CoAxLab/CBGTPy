from common.tracetype import *


def duplicate(df, label, opts):
    numcopies = len(opts)
    dflen = len(df)
    dfnew = df.loc[df.index.repeat(numcopies)]
    dfnew = dfnew.reset_index(drop=True)
    dfnew[label] = pd.concat([pd.Series(opts)] * dflen, ignore_index=True)
    return dfnew


def DataFrameFromDict(data):
    # conversion from a dictionary of column:values
    # returns a dataframe
    try:
        return pd.DataFrame.from_dict(data)
    except BaseException:
        for key, value in data.items():
            if not isinstance(value, list):
                data[key] = [value]
        return pd.DataFrame.from_dict(data)


def ParamSet(orig, df):
    # labeling a dataframe according to an origin
    if isinstance(df, dict):
        df = DataFrameFromDict(df)
    df = df.reset_index(drop=True)
    df = trace(df, orig)
    return df


def ModifyViaSelector(df, template, selector=None, orig='mvs'):
    # use a selector to select specific lines from a dataframe, and then replace those lines with new lines based on a template
    #   - can insert multiple new lines for each original line
    #   - template dataframe can specific unique modified values for each row
    #   - returns the new dataframe
    df = df.copy()
    template = template.copy()
    #print(template.columns)
    for key in template.keys():
        if key not in df.columns:
            df[key] = np.nan
    newdf = pd.DataFrame(columns=df.columns)
    validselector = False
    for idx, row in df.iterrows():
        if selector is None or selector(row):
            validselector = True
            modified = template.copy()
            for col in row.index:
                if col not in template.columns:
                    modified[col] = row[col]
            if len(modified.merge(newdf)) == len(modified): #for action channels - do not copy the modified df if the new df is already correct
                continue
            else:
                newdf = pd.concat([newdf, modified]) #newdf.append(modified) 
        else:
            newdf = pd.concat([newdf, row.to_frame().transpose()]) #newdf.append(row) 
    if not validselector:
        raise Exception("The selector didn't select anything!")
    newdf = newdf.reset_index(drop=True)
    newdf = trace(newdf, orig)
    return newdf


def OptSelector(optinfo, extra=None):
    # generate a selector based on keys to lists of options
    #   - the selector is such that it returns true for any row in a dataframe where the value in each column in a set of columns is a value from a list of options (a different list for each column)
    #   - return the selector
    if not isinstance(optinfo, dict):
        optinfo = {optinfo: extra}

    def Selector(series):
        for key, value in optinfo.items():
            try:
                if series[key] not in value:
                    return False
            except BaseException:
                if series[key] != value:
                    return False
        return True
    return Selector


def GenSinglePropertySelector(prop):
    # given a name of a property (column name), produce a SinglePropertySelector for that column
    #   - returns the SinglePropertySelector
    def SinglePropertySelector(opts):
        # given a list of options, returns an OptSelector for the column to those options
        #   - returns a Selector
        return OptSelector(prop, opts)
    return SinglePropertySelector


SelName = GenSinglePropertySelector('name')


def constructSquareDf(ids):
    # from list of IDs, create a square dataframe with those rows and columns
    return pd.DataFrame(np.zeros((len(ids), len(ids))), index=ids, columns=ids)


def FullBiselector(selectsrc, selectdest):
    # return a biselector that's an all-to-all mapping between two selectors
    def Biselector(srcrow, destrow):
        return selectsrc(srcrow) and selectdest(destrow)
    return Biselector


def MatchBiselector(selectsrc, selectdest, matchprops=[]):
    # return a biselector similar to a FullBiselector but requiring that the
    # source and destination both have equal values at a list of column names
    def Biselector(srcrow, destrow):
        try:
            for prop in matchprops:
                # if not srcrow[prop].is_nan() and not destrow[prop].is_nan():
                if srcrow[prop] != destrow[prop]:
                    return False
        except BaseException:
            if srcrow[matchprops] != destrow[matchprops]:
                return False
        return selectsrc(srcrow) and selectdest(destrow)
    return Biselector


def NamePathwaySelector(srcname, destname, matchprops=[]):
    return MatchBiselector(SelName(srcname), SelName(destname), matchprops)


def FillGridSelection(grid, df, biselector, fillvalue):
    # fill a grid dataframe with a specific value when the row/column fulfills the biselector's condition
    #   - is used to fill in efficacies and connection probabilities between source and destination populations
    grid = grid.copy()
    validselector = False
    for idx1, row1 in df.iterrows():
        for idx2, row2 in df.iterrows():
            if biselector(row1, row2):
                validselector = True
                grid.iloc[idx1, idx2] = fillvalue
    if not validselector:
        raise Exception("The selector didn't select anything!")
    return grid
