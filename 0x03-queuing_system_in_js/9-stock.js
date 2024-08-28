const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

function getItemById(id) {
    return listProducts.find(product => product.id === id);
}

const express = require('express');
const app = express();
const port = 1245;

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient();

const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const getAsync = promisify(client.get).bind(client);
  const stock = await getAsync(`item.${itemId}`);
  return stock !== null ? parseInt(stock, 10) : null;
};

app.get('/list_products', (req, res) => {
    const products = listProducts.map(product => ({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
    }));
    res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);
  
    if (!product) {
      return res.json({ status: 'Product not found' });
    }
  
    const currentStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = currentStock !== null ? product.stock - currentStock : product.stock;
  
    res.json({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity,
    });
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);
  
    if (!product) {
      return res.json({ status: 'Product not found' });
    }
  
    const currentStock = await getCurrentReservedStockById(itemId);
    const availableStock = currentStock !== null ? product.stock - currentStock : product.stock;
  
    if (availableStock <= 0) {
      return res.json({ status: 'Not enough stock available', itemId });
    }
  
    reserveStockById(itemId, (currentStock || 0) + 1);
    res.json({ status: 'Reservation confirmed', itemId });
  });
  