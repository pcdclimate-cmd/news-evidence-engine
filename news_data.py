"""Clearly fictional editorial fixtures. NOT current news or a verified news feed."""
COUNTRIES = {
 'SE':('Sverige','Sweden', ['Demo: Ny energistudie presenteras för byggnadssektorn','Demo: Universitet öppnar nytt forskningssamarbete']),
 'DK':('Danmark','Denmark',['Demo: Kommun testar nytt system för energilagring','Demo: Forskare presenterar metod för kustövervakning']),
 'NO':('Norge','Norway',['Demo: Pilotprojekt undersöker utsläpp från transporter','Demo: Myndighet föreslår förändrad datarapportering']),
 'FI':('Finland','Finland',['Demo: Forskargrupp studerar vinterberedskap','Demo: Ny studie undersöker industrins elbehov']),
 'DE':('Tyskland','Germany',['Demo: Forskare jämför industriella värmelösningar','Demo: Städer provar öppna trafikdata']),
 'FR':('Frankrike','France',['Demo: Forskningsinstitut publicerar klimatmetodik','Demo: Region testar nytt regionalt transportsystem']),
 'GB':('Storbritannien','United Kingdom',['Demo: Universitet lanserar studie om hälsa och luft','Demo: Forskargrupp analyserar vattenförsörjning']),
 'US':('USA','United States of America',['Demo: Energilaboratorium presenterar försöksresultat','Demo: Universitetsnätverk lanserar datainitiativ']),
 'CA':('Kanada','Canada',['Demo: Naturvårdsprojekt offentliggör mätserie','Demo: Regional forskningssatsning på batteriteknik']),
 'BR':('Brasilien','Brazil',['Demo: Universitet studerar förändringar i regnskog','Demo: Forskningsgrupp presenterar analys av jordbruk']),
 'ZA':('Sydafrika','South Africa',['Demo: Energiprojekt undersöker lokal nätdrift','Demo: Vattenforskare presenterar ny mätmetod']),
 'IN':('Indien','India',['Demo: Forskningsstudie mäter stadsluftens kvalitet','Demo: Pilotprojekt testar nya transportsystem']),
 'CN':('Kina','China',['Demo: Laboratorium publicerar materialstudie','Demo: Forskargrupp undersöker lagring av energi']),
 'JP':('Japan','Japan',['Demo: Forskargrupp testar jordbävningssensorer','Demo: Ny prototyp för industriell återvinning']),
 'AU':('Australien','Australia',['Demo: Forskare undersöker marina temperaturer','Demo: Pilotstudie om torka och vattenlager']),
 'UA':('Ukraina','Ukraine',['Demo: Universitet utvecklar öppna geodata','Demo: Forskargrupp studerar infrastrukturens återhämtning']),
 'ES':('Spanien','Spain',['Demo: Energilabb testar värmelagring','Demo: Ny studie om vattenåtervinning']),
 'IT':('Italien','Italy',['Demo: Forskningsinstitut testar stadsklimatmodell','Demo: Universitet analyserar historiska mätserier']),
 'PL':('Polen','Poland',['Demo: Pilotprojekt studerar återbruk i industrin','Demo: Forskargrupp kartlägger elnätets flexibilitet']),
 'MX':('Mexiko','Mexico',['Demo: Forskningsprogram mäter grundvattennivåer','Demo: Studie jämför metoder för renare stadsluft']),
}

def country_news(code):
    code=code.upper()
    if code not in COUNTRIES:return {'country_code':code,'mode':'demo','stories':[]}
    name,english,headlines=COUNTRIES[code]
    return {'country_code':code,'country':name,'english_name':english,'mode':'demo','methodology':'Två fiktiva demonstrationsrubriker. Ingen redaktionell rankning eller verifiering utförd.',
      'stories':[{'id':f'{code}-{i+1}','headline':h,'rank':i+1,'status':'Ej granskad','source':None,'author':None,'published_at':None,'cluster_id':None} for i,h in enumerate(headlines)]}
