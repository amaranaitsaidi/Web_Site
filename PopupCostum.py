import folium


def popup(val1,val2,val3,val4,val5):
    """
    Fonction qui rempli un template HTML avec une variable texte
    :param valeur: objet de type str
    :return: str code html
    """
    return """
<table style="width: 200px">
    <tr>
        <td><strong>Date de signalement : </strong>{}</td>
    </tr>
     <tr>
        <td><strong>Sexe de la piqure  : </strong>{}</td>
    </tr>
     <tr>
        <td><strong>Environnement : </strong>{}</td>
    </tr>
    <tr>
        <td><strong>Raison de présence sur le lieu : </strong>{}</td>
    </tr>
    <tr>
        <td><strong>Departement : </strong>{}</td>
    </tr>
</table>
""".format(val1,val2,val3,val4,val5)