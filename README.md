# 1l1 - des liens qui changent des vies

Cette application web sera accessible ici : [https://1l1.link](https://1l1.link) (bientôt).  
### Description : Un raccourcisseur de liens

Cette application web est un raccourcisseur de liens, similaire à Bitly ou au raccourcisseur de liens de LinkedIn.

---

## **POURQUOI**  
Ce projet est né d'un besoin personnel. J'avais besoin d'un raccourcisseur de liens pour ma marque personnelle sur les réseaux sociaux. J'ai décidé de relever ce défi en construisant cette application.

---

## **FONCTIONNALITÉS**  

### **Page d'accueil**  
Accessible via le chemin `/`.  
L'utilisateur est redirigé vers la page `/show`. Cependant, l'utilisateur doit être connecté pour y accéder.

---

### **Inscription**  
Accessible via le chemin `/register`.  

L'utilisateur peut créer un compte en renseignant un nom d'utilisateur, une adresse e-mail, un mot de passe et en confirmant ce mot de passe. Si les mots de passe ne correspondent pas, si le nom d'utilisateur est déjà pris ou si les champs obligatoires sont vides, l'utilisateur ne pourra pas créer un compte.

La fonction `check_email` vérifie la validité de l'adresse e-mail à l'aide d'une expression régulière. Si l'adresse est incorrecte, l'utilisateur recevra un message d'erreur et ne pourra pas s'inscrire.

Le mot de passe est haché avant d'être enregistré dans la base de données. Une fois inscrit avec succès, l'utilisateur reçoit 100 crédits pour créer des liens raccourcis et peut se connecter à son compte.

---

### **Connexion**  
Accessible via le chemin `/login`.  

Pour se connecter, l'utilisateur doit saisir ses identifiants (nom d'utilisateur et mot de passe). Si ces informations sont incorrectes ou manquantes, l'utilisateur ne pourra pas accéder à son compte.

La comparaison se fait entre le mot de passe haché enregistré dans la base de données et le haché du mot de passe saisi. Si les deux ne correspondent pas, une page d'erreur s'affiche.

En cas de succès, l'ID et le nom d'utilisateur de l'utilisateur sont stockés dans la session du navigateur, et l'utilisateur est connecté.

---

### **Déconnexion**  
Accessible via le chemin `/logout`.  

Lorsqu'un utilisateur clique sur le bouton de déconnexion, une confirmation est demandée. Après déconnexion, il ne peut plus voir ni créer de liens raccourcis. La session du navigateur est également effacée.

---

### **Afficher (Liste)**  
Accessible via le chemin `/show`.  

Affiche le nombre de crédits restants, la dernière connexion (en jours) et la liste de tous les liens raccourcis créés par l'utilisateur connecté. Chaque ligne contient des détails comme le titre, le nombre de vues, la description, le lien original et le lien raccourci (cliquables).

---

### **Créer**  
Accessible via le chemin `/create`.  

Permet à l'utilisateur de créer un lien raccourci après validation des données : titre, description, user_id, et vérification de la validité du lien original via la fonction `check_url`.  

**Coûts des crédits pour les liens :**
- Lien personnalisé : 5 crédits.
- Lien aléatoire : de 1 à 4 crédits selon la longueur (7 caractères = 1 crédit, 6 caractères = 2 crédits, etc.).

Si l'utilisateur n'a pas assez de crédits, il ne peut pas créer de lien.

---

### **Redirection**  
Accessible via le chemin `/link/[slug]`.  

Lorsqu'un utilisateur accède à un slug, le système vérifie si ce slug correspond à un lien dans la base de données. Si oui :
1. Le nombre de vues est incrémenté.
2. L'utilisateur est redirigé vers le lien original.

Sinon, une page d'erreur s'affiche pour signaler que le slug est invalide.

---

Si vous le souhaitez, je peux transformer ce contenu en un fichier Word. Dois-je le faire ?
