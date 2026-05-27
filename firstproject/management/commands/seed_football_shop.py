from decimal import Decimal

from django.core.management.base import BaseCommand

from firstproject.models import (
    Brand,
    Category,
    Club,
    Customer,
    Order,
    OrderItem,
    Product,
    Supplier,
)


class Command(BaseCommand):
    help = "Заполняет базу демонстрационными данными магазина футбольной атрибутики."

    def handle(self, *args, **options):
        categories = {
            "form": Category.objects.get_or_create(
                slug="form",
                defaults={
                    "name": "Форма",
                    "description": "Игровые футболки и комплекты для тренировок.",
                },
            )[0],
            "scarves": Category.objects.get_or_create(
                slug="scarves",
                defaults={
                    "name": "Шарфы",
                    "description": "Клубные шарфы для матчей и коллекций.",
                },
            )[0],
            "balls": Category.objects.get_or_create(
                slug="balls",
                defaults={
                    "name": "Мячи",
                    "description": "Тренировочные и сувенирные футбольные мячи.",
                },
            )[0],
            "boots": Category.objects.get_or_create(
                slug="boots",
                defaults={
                    "name": "Бутсы",
                    "description": "Обувь для игры на натуральном и искусственном газоне.",
                },
            )[0],
        }

        clubs = {
            "spartak": Club.objects.get_or_create(
                name="Спартак Москва",
                defaults={
                    "country": "Россия",
                    "league": "Российская Премьер-Лига",
                    "logo": "firstproject/img/logo-club.svg",
                    "description": "Атрибутика московского футбольного клуба Спартак.",
                },
            )[0],
            "barcelona": Club.objects.get_or_create(
                name="Барселона",
                defaults={
                    "country": "Испания",
                    "league": "Ла Лига",
                    "logo": "firstproject/img/logo-club.svg",
                    "description": "Атрибутика футбольного клуба Барселона.",
                },
            )[0],
            "universal": Club.objects.get_or_create(
                name="Без клубной привязки",
                defaults={
                    "country": "Разные страны",
                    "league": "Универсальная экипировка",
                    "logo": "firstproject/img/logo-club.svg",
                    "description": "Товары для футбола без привязки к конкретной команде.",
                },
            )[0],
        }

        brands = {
            "spartak": Brand.objects.get_or_create(
                name="ФК Спартак",
                defaults={
                    "country": "Россия",
                    "logo": "firstproject/img/logo-brand.svg",
                    "description": "Клубная продукция футбольного клуба Спартак.",
                },
            )[0],
            "barcelona": Brand.objects.get_or_create(
                name="FC Barcelona",
                defaults={
                    "country": "Испания",
                    "logo": "firstproject/img/logo-brand.svg",
                    "description": "Клубная продукция футбольного клуба Барселона.",
                },
            )[0],
            "adidas": Brand.objects.get_or_create(
                name="Adidas",
                defaults={
                    "country": "Германия",
                    "logo": "firstproject/img/logo-brand.svg",
                    "description": "Производитель футбольной обуви, формы и инвентаря.",
                },
            )[0],
        }

        suppliers = {
            "fanopt": Supplier.objects.get_or_create(
                name="FanOpt",
                defaults={
                    "city": "Москва",
                    "email": "sales@fanopt.example",
                    "phone": "+7 900 100-20-30",
                    "description": "Оптовый поставщик клубной атрибутики и сувениров.",
                },
            )[0],
            "goaltrade": Supplier.objects.get_or_create(
                name="GoalTrade",
                defaults={
                    "city": "Санкт-Петербург",
                    "email": "order@goaltrade.example",
                    "phone": "+7 900 300-40-50",
                    "description": "Поставщик тренировочной экипировки, мячей и аксессуаров.",
                },
            )[0],
        }

        products_data = [
            {
                "slug": "zenit-home-jersey",
                "name": "Домашняя форма Спартак",
                "category": categories["form"],
                "club": clubs["spartak"],
                "brand": brands["spartak"],
                "supplier": suppliers["fanopt"],
                "price": Decimal("5490.00"),
                "stock": 18,
                "photo": "firstproject/img/spartak-home-kit.jpg",
                "short_description": "Красно-белая домашняя форма московского Спартака.",
                "description": "Домашняя форма Спартака с клубной символикой. Подходит для матч-дней, коллекции болельщика и повседневной футбольной стилистики.",
            },
            {
                "slug": "real-scarf-classic",
                "name": "Шарф Барселоны",
                "category": categories["scarves"],
                "club": clubs["barcelona"],
                "brand": brands["barcelona"],
                "supplier": suppliers["fanopt"],
                "price": Decimal("1890.00"),
                "stock": 35,
                "photo": "firstproject/img/barcelona-scarf.jpg",
                "short_description": "Фанатский шарф футбольного клуба Барселона.",
                "description": "Шарф Барселоны для болельщиков клуба. Подходит для стадиона, коллекции и подарка фанату каталонской команды.",
            },
            {
                "slug": "milan-training-ball",
                "name": "Футбольный мяч Adidas Trionda Pro ЧМ 2026",
                "category": categories["balls"],
                "club": clubs["universal"],
                "brand": brands["adidas"],
                "supplier": suppliers["goaltrade"],
                "price": Decimal("2490.00"),
                "stock": 22,
                "photo": "firstproject/img/adidas-trionda-2026-ball.jpg",
                "short_description": "Официальный футбольный мяч чемпионата мира 2026.",
                "description": "Футбольный мяч Adidas Trionda Pro, выполненный в стилистике чемпионата мира FIFA 2026. Подходит для коллекции и игры.",
            },
            {
                "slug": "prokick-speed-boots",
                "name": "Футбольные бутсы Adidas Predator Freak.1 FG",
                "category": categories["boots"],
                "club": clubs["universal"],
                "brand": brands["adidas"],
                "supplier": suppliers["goaltrade"],
                "price": Decimal("6990.00"),
                "stock": 11,
                "photo": "firstproject/img/adidas-predator-boots.jpg",
                "short_description": "Бутсы Adidas Predator для игры на натуральном газоне.",
                "description": "Футбольные бутсы Adidas Predator Freak.1 FG с ярким дизайном и шипами для натурального газона. Подходят для тренировок и матчей.",
            },
        ]

        products = {}
        for data in products_data:
            product, _ = Product.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            products[data["slug"]] = product

        customer, _ = Customer.objects.get_or_create(
            email="ivan.petrov@example.com",
            defaults={
                "first_name": "Иван",
                "last_name": "Петров",
                "phone": "+7 900 555-10-10",
            },
        )

        order, _ = Order.objects.get_or_create(
            customer=customer,
            delivery_address="Москва, ул. Футбольная, 7",
            defaults={"status": Order.STATUS_PAID},
        )
        OrderItem.objects.update_or_create(
            order=order,
            product=products["zenit-home-jersey"],
            defaults={"quantity": 1, "price": products["zenit-home-jersey"].price},
        )
        OrderItem.objects.update_or_create(
            order=order,
            product=products["real-scarf-classic"],
            defaults={"quantity": 2, "price": products["real-scarf-classic"].price},
        )

        Club.objects.filter(products__isnull=True).exclude(
            name__in=["Спартак Москва", "Барселона", "Без клубной привязки"]
        ).delete()
        Brand.objects.filter(products__isnull=True).exclude(
            name__in=["ФК Спартак", "FC Barcelona", "Adidas"]
        ).delete()

        self.stdout.write(self.style.SUCCESS("Демонстрационные данные добавлены."))
