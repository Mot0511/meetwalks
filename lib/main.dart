import 'package:flutter/material.dart';
import 'features/home/screens/home_screen.dart';
import 'theme.dart';

void main() {
  runApp(const Meetwalks());
}

class Meetwalks extends StatelessWidget {
  const Meetwalks({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(theme: theme, home: const HomeScreen());
  }
}
