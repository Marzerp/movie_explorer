// Crear DB y usuarios personalizados
db = db.getSiblingDB(process.env.MONGO_APP_DB);

db.createUser({
  user: process.env.MONGO_APP_USER,
  pwd: process.env.MONGO_APP_PASSWORD,
  roles: [{ role: 'readWrite', db: process.env.MONGO_APP_DB},
          { role: 'dbAdmin', db: process.env.MONGO_APP_DB}, ]
});
