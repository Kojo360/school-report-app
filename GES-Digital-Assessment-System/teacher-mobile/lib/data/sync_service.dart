import 'dart:convert';

import 'package:http/http.dart' as http;

import 'local_database.dart';

/// Sends locally queued records to the FastAPI /sync endpoint when online.
class SyncService {
  SyncService({required this.baseUrl, required this.accessToken});

  final String baseUrl;
  final String accessToken;

  Future<int> syncPending() async {
    final jobs = await LocalDatabase.instance.getPendingSyncJobs();
    if (jobs.isEmpty) return 0;

    final response = await http.post(
      Uri.parse('$baseUrl/sync'),
      headers: {'Authorization': 'Bearer $accessToken', 'Content-Type': 'application/json'},
      body: jsonEncode({
        'items': jobs.map((job) => {
          'local_id': job['id'],
          'entity_type': job['entity_type'],
          'action': job['action'],
          'payload': jsonDecode(job['payload']! as String),
        }).toList(),
      }),
    );
    if (response.statusCode != 200) return 0;

    var synced = 0;
    for (final result in (jsonDecode(response.body)['items'] as List<dynamic>)) {
      if (result['sync_status'] == 'SYNCED') {
        await LocalDatabase.instance.markSyncJobSynced(result['local_id'] as int);
        synced++;
      }
    }
    return synced;
  }
}
