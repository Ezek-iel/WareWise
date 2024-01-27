import models

testCategory  = models.Category(name = "Food", description = "A food category")

testProducts = models.Product(name = "Food SPX1", category = testCategory)
