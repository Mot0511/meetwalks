import 'dart:ui';
import 'package:flutter/material.dart';

class SearchWidget extends StatelessWidget {
  const SearchWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {},
      style: ElevatedButton.styleFrom(
        shape: CircleBorder(),
        disabledForegroundColor: Colors.amber,
        fixedSize: Size(150, 150),
        backgroundColor: Colors.lightBlue.withValues(alpha: 0.6),
        foregroundColor: Colors.lightBlue,
      ),
      child: Icon(Icons.search, size: 100, color: Colors.white),
    );
  }
}