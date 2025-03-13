import 'package:flutter/material.dart';
import 'package:meetwalks/features/home/utils/time_util.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    getTimeNow();
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/backgrounds/bg_day.jpg"),
            fit: BoxFit.cover,
          ),
        ),
        child: Column(
          children: [
            Padding(
              padding: EdgeInsets.all(10),
              child: Container(
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.white.withOpacity(0.6)),
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white.withOpacity(0.6),
                ),
                height:
                    MediaQuery.of(context).size.height /
                    15, // Высота панели 1/15 экрана
                padding: EdgeInsets.symmetric(
                  vertical: 10.0,
                  horizontal: 20.0,
                ), // Отступы
                // ignore: deprecated_member_use
                //color: Colors.white.withOpacity(0.4),// Цвет панели
                child: Row(
                  mainAxisAlignment:
                      MainAxisAlignment.spaceBetween, // Распределение элементов
                  children: [
                    Text(
                      nowTime,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    Text(
                      'Meetwalks!',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                    Text(
                      '25.C',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 25,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: MediaQuery.of(context).size.height / 7),
            ElevatedButton(
              onPressed: () {
                print("asdas");
              },
              style: ElevatedButton.styleFrom(
                shape: CircleBorder(),
                fixedSize: Size(150, 150),
                backgroundColor: Colors.white.withOpacity(0.6),
                foregroundColor: Colors.white.withOpacity(0.6),
              ),
              child: Icon(Icons.search, size: 100, color: Colors.white),
            ),
            SizedBox(height: 23),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                fixedSize: Size(130, 40),
                backgroundColor: Colors.white.withOpacity(0.6),
                foregroundColor: Colors.white.withOpacity(0.6),
                iconSize: 40,
              ),
              child: Icon(Icons.settings, color: Colors.white, size: 20),
            ),
          ],
        ),
      ),
    );
  }
}
