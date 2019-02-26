import matplotlib.colors as clr
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import squarify 

def init_setup():

    sns.set(rc={'figure.figsize':(15,8)})
    sns.set(style="white", context="talk")
   
    
def genre_pie(genre_counts, genre_list, name):

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(genre_counts)

    #Compute percentages
    pct = 100*genre_counts/len(genre_list)

    ax.legend(labels=['%s  %1.2f %%' % (l, s) for l, s in zip(list(pct.keys()), list(pct))], loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title(name)
    plt.show()
    
    
def genre_bar(genre_counts, genre_list, name): 
    
    total = float(len(genre_list))
    ax = sns.barplot(x=genre_counts, y=genre_counts.keys(), orient='h', palette='PuBu_r')

    #Compute and locate percentages
    for p in ax.patches:
        loc = ax.patches[0].get_width()
        width = p.get_width()
        ax.text(loc+ 20, p.get_y()+p.get_height()/1.5, '  '+'{:1.2f}'.format(100*width/total) + '%', ha='left') 
        
    ax.set_xticks([])
    sns.despine(left=True, bottom=True)
    plt.show()


def genre_map(genre_counts, genre_list, name, th):

    # Creating colorscheme
    cmap = cm.Blues
    mini=min(np.array(genre_counts))
    maxi=max(np.array(genre_counts))
    norm = clr.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in np.array(genre_counts)]

    other = 0
    x = np.array(genre_counts)
    y = np.array(genre_counts.keys())

    if th > 0:
        for el in x:
            
            pct = 100*el/float(len(genre_list))
            
            if pct < th:
                other += el
                i = np.where(x == el)
                x = np.delete(x, i, 0)
                y = np.delete(y, i, 0)
                
        x = np.append(x, other)
        y = np.append(y, 'other')

    squarify.plot(sizes=x, label=y, alpha=.8, color=colors)
    plt.axis('off')
    plt.title(name)
    plt.show() 
    
    
def genre_mood_bar(mood, genre_counts, pct, name): 
    
    ax = sns.barplot(x=genre_counts.keys(), y=genre_counts, hue=mood, palette='Paired')

    i = 0
    for p in ax.patches:
        ax.text(p.get_x()+p.get_width()/2., p.get_height() + 10., '{:1.2f}'.format(pct[i]) + '%', ha='center', fontsize=15) 
        i += 1

    ax.set_xlabel(name)
    ax.set_ylabel('count')
    sns.despine(left=True, bottom=True)
    
    
def features_gen_box(g_dict, l_dict, name):
    
    x = []
    y = []
    for mbid in g_dict:

        if mbid in l_dict: 
            x.append(g_dict[mbid])
            y.append(l_dict[mbid])
    
    ax = sns.boxplot(x=np.array(x), y=np.array(y), palette='Set3')
    sns.despine(left=True, bottom=True)
    ax.set_xlabel('genre_rosamerica')
    ax.set_ylabel('average_loudness')
    ax.set_title(name)
    
    
def set_year_labels(ax):

    labels = []

    for label in ax.get_xticklabels():
        if label not in ax.get_xticklabels()[0::5]:
            labels.append(plt.text(0, 0, ''))
        else:
            labels.append(label)
            
    return labels


def year_bar(year_counts, year_keys, quantiles):
    
    plt.figure(figsize=(18,6))

    ax = sns.barplot(x=year_keys, y=year_counts, palette='GnBu')

    labels = set_year_labels(ax)

    ax.set_xticklabels(labels, ha="center")

    plt.axvline(quantiles[0.25], 0, 1)
    plt.axvline(quantiles[0.50], 0, 1)
    plt.axvline(quantiles[0.75], 0, 1)

    plt.ylabel('count')
    plt.xlabel('year')
    sns.despine(left=True, bottom=True)
    plt.show()
    
    
def features_years_box(y_dict, l_dict, name):
    
    x = []
    y = []
    for mbid in y_dict:

        if mbid in l_dict and y_dict[mbid] >= 1950.0: 
            x.append(y_dict[mbid])
            y.append(l_dict[mbid]) 

    x_int = np.array(x).astype(int)
    
    plt.figure(figsize=(18,6))
    ax = sns.boxplot(x=x_int, y=np.array(y), color='xkcd:lightblue')
    
    labels = set_year_labels(ax)
    
    ax.set_xticklabels(labels, ha="center")

    plt.ylabel(name)
    plt.xlabel('year')
    sns.despine(left=True, bottom=True)
    plt.show()
    
    
def key_est_bar(keys, key_counts):
    
    #Compute percentages
    a = key_counts[0 : int(len(key_counts)/2)].values
    b = key_counts[int(len(key_counts)/2):].values

    pct = 100 * a / (a+b)
    pct = np.append(pct, 100 - pct)
    
    ax = sns.barplot(x=np.array(keys[1]), y=key_counts, hue=np.array(keys[0]), palette='Paired')

    i = 0
    for p in ax.patches:
        ax.text(p.get_x()+p.get_width()/2., p.get_height() + 10., '{:1.2f}'.format(pct[i]) + '%', ha='center', fontsize=14) 
        i += 1

    ax.set_xlabel('tonic')
    ax.set_ylabel('count')
    sns.despine(left=True, bottom=True)