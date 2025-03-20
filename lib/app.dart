import 'package:flutter/material.dart';
import 'package:meetwalks/features/groups/groups.dart';
import 'package:meetwalks/features/home/screens/home_screen.dart';
import 'package:meetwalks/theme.dart';
import 'package:meetwalks/widgets/NavBar.dart';

class Meetwalks extends StatefulWidget {
  const Meetwalks({super.key});

  @override
  State<Meetwalks> createState() => _MeetwalksState();
}

class _MeetwalksState extends State<Meetwalks> {

  int page = 0;

  final List<Widget> screens = [
    HomeScreen(),
    GroupScreen(),
  ]; 

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: theme,
      home: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/backgrounds/bg_night.jpg"),
            fit: BoxFit.cover,
          ),
        ),
        child: Scaffold(
          body: screens[page],
          bottomNavigationBar: Navbar(
            onTap: (index) => setState(() => page = index)
          ),
        )
      ),
    );
  }
}