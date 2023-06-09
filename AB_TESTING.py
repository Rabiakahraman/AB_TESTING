#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("4.hafta Measurement/ödevler/ABTesti/ab_testing.xlsx", "Control Group")
df_test = pd.read_excel("4.hafta Measurement/ödevler/ABTesti/ab_testing.xlsx", "Test Group")



# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
def check_df(dataframe):
    print(dataframe.shape)
    print(dataframe.dtypes)
    print(dataframe.head())
    print(dataframe.tail())
    print(dataframe.describe().T)
check_df(df_test)
check_df(df_control)
# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_conc = pd.concat([df_control, df_test], axis=0, ignore_index=True)

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
#HO : M1 = M2
#H1 : M1 ! M2

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz
print(f"Control Group Mean: {df_control['Purchase'].mean()} \nTest Group Mean: {df_test['Purchase'].mean()}")

df_control.groupby("Purchase").mean().reset_index()

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz
# Normallik varsayımı:
# H0: Dağılım normaldir.        P-value < 0.05 ise RED
# H1: Dağılım normal değildir.  P-value > 0.05 ise RED

def normal_check(group_name, test=False):
    if test:
       shap_stat, pvalue = shapiro(df_test[group_name])
       print("p_value %.4f" % (pvalue))
    else:
       shap_stat, pvalue = shapiro(df_control[group_name])
       print("p_value %.4f" % (pvalue))

normal_check("Purchase")
normal_check("Purchase", test=True)

# Varyans homojenliği varsayımı:
# H0: Varyanslar homojen dağılmıştır.   P-value < 0.05 ise RED
# H1: Dağılmamıştır.                    P-value > 0.05 ise RED

def var_check(group_name_1, group_name_2):
    var_stat, pvalue = levene(df_test[group_name_1],
                              df_control[group_name_2])
    print("p_value %.4f" % (pvalue))

var_check("Purchase", "Purchase")



# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz
"""Hem normallik varsayımı hem de varyans homojenliği sağlanmıştır. Bu durumda parametric
   test uygulanmalıdır."""

non_stats, pvalue = ttest_ind(df_control["Purchase"], df_test["Purchase"], equal_var=True)
print("p_value %.4f" % (pvalue))

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

"""Test sonucunda elde edilen p_value değeri 0.05'ten büyüktür. 
   Bu durumda H0 hipotezi geçerlidir yani iki durum arasında istatistiksel olarak bir
   anlam farkı yoktur."""

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
"""Normallik varsayımı için Shapiro-Wilk testini,
   Varyans Homojenliği varsayımı için ise Levene testini kullandım.
   Bu testler sonucunda p_value değeri 0.05'ten yüksek geldiği ve
   varsayımlar sağlandığı için, parametric test kullanarak AB testing işlemini tamamladım."""



# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
"""Yapılan test çalışmasına göre, her ne kadar test ve kontrol gruplarının satış ortalamaları
   arasında 32 birim gibi dikkate alınabilecek bir fark olsa da, bu farkın istatistiğe dayalı bir
   anlam ifade etmediği incelendi. Yani, ortalamalar arasındaki farkın, bu güncellemeden farklı etkenlere
   dayalı olarak, şansa bağlı geliştiği söylenebilir. İki grup arasında bulunan fark dönemsel etkilere, 
   farklı güncellemelere ve süreçlere dayanıyor olabilir. 

   Özetle, yeni Average Bidding kullanımının, Max Bidding üzerinde getiri olarak açıkça bir üstünlüğü olmadığı
   gözlemlenmektedir."""
