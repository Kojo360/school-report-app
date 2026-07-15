import 'dart:convert';

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

/// SQLite persistence for offline student records, grades, and sync jobs.
class LocalDatabase {
  LocalDatabase._();

  static final LocalDatabase instance = LocalDatabase._();
  Database? _database;

  Future<Database> get database async {
    final existing = _database;
    if (existing != null) return existing;

    final path = join(await getDatabasesPath(), 'ges_teacher_mobile.db');
    _database = await openDatabase(path, version: 1, onCreate: _createDatabase);
    return _database!;
  }

  Future<void> _createDatabase(Database db, int version) async {
    await db.execute('''
      CREATE TABLE local_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        admission_date TEXT NOT NULL,
        sync_status TEXT NOT NULL DEFAULT 'PENDING'
      )
    ''');
    await db.execute('''
      CREATE TABLE local_grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        score REAL NOT NULL,
        sync_status TEXT NOT NULL DEFAULT 'PENDING',
        FOREIGN KEY(student_id) REFERENCES local_students(id)
      )
    ''');
    await db.execute('''
      CREATE TABLE sync_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        payload TEXT NOT NULL,
        sync_status TEXT NOT NULL DEFAULT 'PENDING',
        created_at TEXT NOT NULL
      )
    ''');
  }

  Future<List<Map<String, Object?>>> getStudents() async {
    final db = await database;
    return db.query('local_students', orderBy: 'full_name');
  }

  Future<void> addStudent({
    required String fullName,
    required String dob,
    required String admissionDate,
  }) async {
    final db = await database;
    final studentId = await db.insert('local_students', {
      'full_name': fullName,
      'dob': dob,
      'admission_date': admissionDate,
      'sync_status': 'PENDING',
    });
    await _queue(db, 'student', studentId, 'CREATE', {
      'id': studentId,
      'full_name': fullName,
      'dob': dob,
      'admission_date': admissionDate,
    });
  }

  Future<void> addGrade({
    required int studentId,
    required String subject,
    required double score,
  }) async {
    final db = await database;
    final gradeId = await db.insert('local_grades', {
      'student_id': studentId,
      'subject': subject,
      'score': score,
      'sync_status': 'PENDING',
    });
    await _queue(db, 'grade', gradeId, 'CREATE', {
      'grade_id': gradeId,
      'student_id': studentId,
      'subject': subject,
      'score': score,
    });
  }

  Future<void> _queue(
    Database db,
    String entityType,
    int entityId,
    String action,
    Map<String, Object> payload,
  ) {
    return db.insert('sync_queue', {
      'entity_type': entityType,
      'entity_id': entityId,
      'action': action,
      'payload': jsonEncode(payload),
      'sync_status': 'PENDING',
      'created_at': DateTime.now().toUtc().toIso8601String(),
    });
  }

  Future<List<Map<String, Object?>>> getPendingSyncJobs() async {
    final db = await database;
    return db.query('sync_queue', where: 'sync_status = ?', whereArgs: ['PENDING'], orderBy: 'id');
  }

  Future<void> markSyncJobSynced(int queueId) async {
    final db = await database;
    await db.update('sync_queue', {'sync_status': 'SYNCED'}, where: 'id = ?', whereArgs: [queueId]);
  }
}
