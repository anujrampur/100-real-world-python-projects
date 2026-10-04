# 100 Real-World Python Projects

Source code for the book **100 Real-World Python Projects: Build Practical Applications from Beginner to Advanced** by Anuj Kumar Saxena.

All 100 programs use only the Python standard library. Nothing extra to install.

## Requirements

- Python 3.10 or newer (syntax-checked on 3.10, run and tested on 3.12 on Linux)
- Tkinter for the GUI projects (included with Python on Windows and macOS; on Debian/Ubuntu: `sudo apt install python3-tk`)

## How to run

```bash
git clone https://github.com/<your-username>/100-real-world-python-projects.git
cd 100-real-world-python-projects/projects
python project_007_unit_conversion_toolkit.py
```

On some systems the command is `python3` or `py`. Project 1 runs in the terminal; all other projects open a Tkinter window.

## Notes

- Project 47 uses the Windows `netsh` command. Project 60 plays sound with `winsound` on Windows and with `afplay`, `paplay` or `aplay` on macOS/Linux (bell only if none is installed). Projects 7, 29, 47, 49 and 60 were also run on Windows.
- Projects 32, 33, 47, 48, 49 and 96 touch the network, files or processes. Use them only on systems you own or are allowed to test.
- Test file-changing projects (21, 45, 48, 95) on copies of your data first.
- The cryptography projects (41, 42, 43, 50, 72) are learning examples. For real applications use well-reviewed libraries.

## Projects


### Section 1: Useful Mini Applications

| # | Project | Level | File |
|---|---|---|---|
| 1 | Personal Expense Tracker | Beginner+ | [project_001_personal_expense_tracker.py](projects/project_001_personal_expense_tracker.py) |
| 2 | Digital Stopwatch | Beginner+ | [project_002_digital_stopwatch.py](projects/project_002_digital_stopwatch.py) |
| 3 | Countdown Timer | Beginner+ | [project_003_countdown_timer.py](projects/project_003_countdown_timer.py) |
| 4 | BMI & Health Calculator | Beginner+ | [project_004_bmi_health_calculator.py](projects/project_004_bmi_health_calculator.py) |
| 5 | Age Calculator | Beginner+ | [project_005_age_calculator.py](projects/project_005_age_calculator.py) |
| 6 | Currency Converter | Beginner+ | [project_006_currency_converter.py](projects/project_006_currency_converter.py) |
| 7 | Unit Conversion Toolkit | Beginner+ | [project_007_unit_conversion_toolkit.py](projects/project_007_unit_conversion_toolkit.py) |
| 8 | Personal Password Generator | Beginner+ | [project_008_personal_password_generator.py](projects/project_008_personal_password_generator.py) |
| 9 | Random Quote Generator | Beginner+ | [project_009_random_quote_generator.py](projects/project_009_random_quote_generator.py) |
| 10 | Personal Notes Manager | Intermediate | [project_010_personal_notes_manager.py](projects/project_010_personal_notes_manager.py) |

### Section 2: Games & Interactive Applications

| # | Project | Level | File |
|---|---|---|---|
| 11 | Rock Paper Scissors | Beginner+ | [project_011_rock_paper_scissors.py](projects/project_011_rock_paper_scissors.py) |
| 12 | Number Guessing Game | Beginner+ | [project_012_number_guessing_game.py](projects/project_012_number_guessing_game.py) |
| 13 | Hangman Classic | Beginner+ | [project_013_hangman_classic.py](projects/project_013_hangman_classic.py) |
| 14 | Tic-Tac-Toe | Beginner+ | [project_014_tic_tac_toe.py](projects/project_014_tic_tac_toe.py) |
| 15 | Quiz Master | Beginner+ | [project_015_quiz_master.py](projects/project_015_quiz_master.py) |
| 16 | Word Scramble | Beginner+ | [project_016_word_scramble.py](projects/project_016_word_scramble.py) |
| 17 | Memory Matching Cards | Intermediate | [project_017_memory_matching_cards.py](projects/project_017_memory_matching_cards.py) |
| 18 | Dice Battle Simulator | Beginner+ | [project_018_dice_battle_simulator.py](projects/project_018_dice_battle_simulator.py) |
| 19 | Classic 2D Snake | Intermediate | [project_019_classic_2d_snake.py](projects/project_019_classic_2d_snake.py) |
| 20 | Typing Speed Tester | Intermediate | [project_020_typing_speed_tester.py](projects/project_020_typing_speed_tester.py) |

### Section 3: Data Analysis & Productivity Tools

| # | Project | Level | File |
|---|---|---|---|
| 21 | Automatic File Organizer | Intermediate | [project_021_automatic_file_organizer.py](projects/project_021_automatic_file_organizer.py) |
| 22 | CSV Data Analyzer & Summary Tool | Intermediate | [project_022_csv_data_analyzer_summary_tool.py](projects/project_022_csv_data_analyzer_summary_tool.py) |
| 23 | Web Page Content Scraper | Intermediate | [project_023_web_page_content_scraper.py](projects/project_023_web_page_content_scraper.py) |
| 24 | Automated PDF Invoice Generator | Intermediate | [project_024_automated_pdf_invoice_generator.py](projects/project_024_automated_pdf_invoice_generator.py) |
| 25 | Excel Spreadsheet Automator | Intermediate | [project_025_excel_spreadsheet_automator.py](projects/project_025_excel_spreadsheet_automator.py) |
| 26 | Bulk Image Resizer & Watermarker | Intermediate | [project_026_bulk_image_resizer_watermarker.py](projects/project_026_bulk_image_resizer_watermarker.py) |
| 27 | Markdown to HTML Converter | Intermediate | [project_027_markdown_to_html_converter.py](projects/project_027_markdown_to_html_converter.py) |
| 28 | Clipboard History Manager | Intermediate | [project_028_clipboard_history_manager.py](projects/project_028_clipboard_history_manager.py) |
| 29 | System Resource Monitor | Intermediate | [project_029_system_resource_monitor.py](projects/project_029_system_resource_monitor.py) |
| 30 | REST API Weather & Forecast Desk | Intermediate | [project_030_rest_api_weather_forecast_desk.py](projects/project_030_rest_api_weather_forecast_desk.py) |

### Section 4: Web Applications & Network Utilities

| # | Project | Level | File |
|---|---|---|---|
| 31 | Lightweight HTTP Web Server | Intermediate | [project_031_lightweight_http_web_server.py](projects/project_031_lightweight_http_web_server.py) |
| 32 | Multi-Threaded TCP Port Scanner | Intermediate | [project_032_multi_threaded_tcp_port_scanner.py](projects/project_032_multi_threaded_tcp_port_scanner.py) |
| 33 | Local Network Ping & Host Discovery | Intermediate | [project_033_local_network_ping_host_discovery.py](projects/project_033_local_network_ping_host_discovery.py) |
| 34 | TCP Peer-to-Peer Chat Room | Advanced | [project_034_tcp_peer_to_peer_chat_room.py](projects/project_034_tcp_peer_to_peer_chat_room.py) |
| 35 | URL Shortener with SQLite Persistence | Intermediate | [project_035_url_shortener_with_sqlite_persistence.py](projects/project_035_url_shortener_with_sqlite_persistence.py) |
| 36 | Automated Website Uptime Monitor | Intermediate | [project_036_automated_website_uptime_monitor.py](projects/project_036_automated_website_uptime_monitor.py) |
| 37 | Email Validator & MX Domain Inspector | Intermediate | [project_037_email_validator_mx_domain_inspector.py](projects/project_037_email_validator_mx_domain_inspector.py) |
| 38 | Fast File Downloader with Progress Bar | Intermediate | [project_038_fast_file_downloader_with_progress_bar.py](projects/project_038_fast_file_downloader_with_progress_bar.py) |
| 39 | REST API Client & HTTP Header Inspector | Intermediate | [project_039_rest_api_client_http_header_inspector.py](projects/project_039_rest_api_client_http_header_inspector.py) |
| 40 | FTP File Browser & Transfer Client | Advanced | [project_040_ftp_file_browser_transfer_client.py](projects/project_040_ftp_file_browser_transfer_client.py) |

### Section 5: Security, Cryptography & Automation

| # | Project | Level | File |
|---|---|---|---|
| 41 | Symmetric File Encryptor & Decryptor | Intermediate | [project_041_symmetric_file_encryptor_decryptor.py](projects/project_041_symmetric_file_encryptor_decryptor.py) |
| 42 | Cryptographic Password Vault | Advanced | [project_042_cryptographic_password_vault.py](projects/project_042_cryptographic_password_vault.py) |
| 43 | Steganography Image Data Hider | Advanced | [project_043_steganography_image_data_hider.py](projects/project_043_steganography_image_data_hider.py) |
| 44 | SHA-256 & MD5 File Integrity Verifier | Intermediate | [project_044_sha_256_md5_file_integrity_verifier.py](projects/project_044_sha_256_md5_file_integrity_verifier.py) |
| 45 | Automated Scheduled Backup Bot | Intermediate | [project_045_automated_scheduled_backup_bot.py](projects/project_045_automated_scheduled_backup_bot.py) |
| 46 | Sensitive Data Redactor & Masker | Intermediate | [project_046_sensitive_data_redactor_masker.py](projects/project_046_sensitive_data_redactor_masker.py) |
| 47 | Wi-Fi Password & Network Profile Viewer | Intermediate | [project_047_wi_fi_password_network_profile_viewer.py](projects/project_047_wi_fi_password_network_profile_viewer.py) |
| 48 | Secure Multi-Pass File Shredder | Intermediate | [project_048_secure_multi_pass_file_shredder.py](projects/project_048_secure_multi_pass_file_shredder.py) |
| 49 | Process Security & Keylogger Audit Tool | Intermediate | [project_049_process_security_keylogger_audit_tool.py](projects/project_049_process_security_keylogger_audit_tool.py) |
| 50 | Two-Factor Authentication (TOTP) Authenticator | Advanced | [project_050_two_factor_authentication_totp_authentic.py](projects/project_050_two_factor_authentication_totp_authentic.py) |

### Section 6: Advanced GUI & Desktop Engineering

| # | Project | Level | File |
|---|---|---|---|
| 51 | Advanced Multi-Tab Text Editor | Advanced | [project_051_advanced_multi_tab_text_editor.py](projects/project_051_advanced_multi_tab_text_editor.py) |
| 52 | Canvas Vector Paint & Drawing Board | Intermediate | [project_052_canvas_vector_paint_drawing_board.py](projects/project_052_canvas_vector_paint_drawing_board.py) |
| 53 | Audio & Video Media Metadata Inspector | Intermediate | [project_053_audio_video_media_metadata_inspector.py](projects/project_053_audio_video_media_metadata_inspector.py) |
| 54 | Kanban Task Management Board | Intermediate | [project_054_kanban_task_management_board.py](projects/project_054_kanban_task_management_board.py) |
| 55 | Interactive Statistical Chart Plotter | Advanced | [project_055_interactive_statistical_chart_plotter.py](projects/project_055_interactive_statistical_chart_plotter.py) |
| 56 | Mathematical Expression Calculator | Intermediate | [project_056_mathematical_expression_calculator.py](projects/project_056_mathematical_expression_calculator.py) |
| 57 | File System Tree & Search Explorer | Intermediate | [project_057_file_system_tree_search_explorer.py](projects/project_057_file_system_tree_search_explorer.py) |
| 58 | Color Palette Studio & Eyedropper | Intermediate | [project_058_color_palette_studio_eyedropper.py](projects/project_058_color_palette_studio_eyedropper.py) |
| 59 | World Timezone Clock HUD | Intermediate | [project_059_world_timezone_clock_hud.py](projects/project_059_world_timezone_clock_hud.py) |
| 60 | Virtual Piano & Audio Synthesizer | Advanced | [project_060_virtual_piano_audio_synthesizer.py](projects/project_060_virtual_piano_audio_synthesizer.py) |

### Section 7: Database Architecture & Data Engineering

| # | Project | Level | File |
|---|---|---|---|
| 61 | Retail Inventory & Stock Management System | Intermediate | [project_061_retail_inventory_stock_management_system.py](projects/project_061_retail_inventory_stock_management_system.py) |
| 62 | Student Gradebook & Relational GPA Calculator | Intermediate | [project_062_student_gradebook_relational_gpa_calcula.py](projects/project_062_student_gradebook_relational_gpa_calcula.py) |
| 63 | Automated Double-Entry Accounting Ledger | Advanced | [project_063_automated_double_entry_accounting_ledger.py](projects/project_063_automated_double_entry_accounting_ledger.py) |
| 64 | Full-Text Search (FTS5) Document Engine | Advanced | [project_064_full_text_search_fts5_document_engine.py](projects/project_064_full_text_search_fts5_document_engine.py) |
| 65 | Relational Schema Migration Engine | Intermediate | [project_065_relational_schema_migration_engine.py](projects/project_065_relational_schema_migration_engine.py) |
| 66 | Database Snapshot & SQL Backup Exporter | Intermediate | [project_066_database_snapshot_sql_backup_exporter.py](projects/project_066_database_snapshot_sql_backup_exporter.py) |
| 67 | Customer Relationship Management (CRM) Pipeline | Intermediate | [project_067_customer_relationship_management_crm_pip.py](projects/project_067_customer_relationship_management_crm_pip.py) |
| 68 | Time-Series Metrics Logger & Query Engine | Intermediate | [project_068_time_series_metrics_logger_query_engine.py](projects/project_068_time_series_metrics_logger_query_engine.py) |
| 69 | JSON-to-Relational Normalizer & Importer | Intermediate | [project_069_json_to_relational_normalizer_importer.py](projects/project_069_json_to_relational_normalizer_importer.py) |
| 70 | Role-Based Access Control (RBAC) System | Advanced | [project_070_role_based_access_control_rbac_system.py](projects/project_070_role_based_access_control_rbac_system.py) |

### Section 8: Web Services, Microservices & APIs

| # | Project | Level | File |
|---|---|---|---|
| 71 | Micro RESTful JSON API Server | Advanced | [project_071_micro_restful_json_api_server.py](projects/project_071_micro_restful_json_api_server.py) |
| 72 | Token-Based Authentication & Session Manager | Advanced | [project_072_token_based_authentication_session_manag.py](projects/project_072_token_based_authentication_session_manag.py) |
| 73 | Rate-Limiting Reverse Proxy & Throttler | Advanced | [project_073_rate_limiting_reverse_proxy_throttler.py](projects/project_073_rate_limiting_reverse_proxy_throttler.py) |
| 74 | Asynchronous Background Task Queue & Worker | Advanced | [project_074_asynchronous_background_task_queue_worke.py](projects/project_074_asynchronous_background_task_queue_worke.py) |
| 75 | Webhook Event Dispatcher & Listener | Intermediate | [project_075_webhook_event_dispatcher_listener.py](projects/project_075_webhook_event_dispatcher_listener.py) |
| 76 | Dynamic Mock API & Response Simulator | Intermediate | [project_076_dynamic_mock_api_response_simulator.py](projects/project_076_dynamic_mock_api_response_simulator.py) |
| 77 | Server-Sent Events (SSE) Real-Time Data Streamer | Advanced | [project_077_server_sent_events_sse_real_time_data_st.py](projects/project_077_server_sent_events_sse_real_time_data_st.py) |
| 78 | API Request Caching Layer with TTL Expiry | Intermediate | [project_078_api_request_caching_layer_with_ttl_expir.py](projects/project_078_api_request_caching_layer_with_ttl_expir.py) |
| 79 | OpenAPI / Swagger Schema Spec Generator | Intermediate | [project_079_openapi_swagger_schema_spec_generator.py](projects/project_079_openapi_swagger_schema_spec_generator.py) |
| 80 | Distributed Health Check & Service Registry Hub | Advanced | [project_080_distributed_health_check_service_registr.py](projects/project_080_distributed_health_check_service_registr.py) |

### Section 9: Machine Learning, Computer Vision & Data Science

| # | Project | Level | File |
|---|---|---|---|
| 81 | Simple Linear Regression & Least Squares Engine | Intermediate | [project_081_simple_linear_regression_least_squares_e.py](projects/project_081_simple_linear_regression_least_squares_e.py) |
| 82 | K-Nearest Neighbors (KNN) Classifier | Intermediate | [project_082_k_nearest_neighbors_knn_classifier.py](projects/project_082_k_nearest_neighbors_knn_classifier.py) |
| 83 | K-Means Unsupervised Clustering Engine | Advanced | [project_083_k_means_unsupervised_clustering_engine.py](projects/project_083_k_means_unsupervised_clustering_engine.py) |
| 84 | Naive Bayes Text & Spam Filter | Intermediate | [project_084_naive_bayes_text_spam_filter.py](projects/project_084_naive_bayes_text_spam_filter.py) |
| 85 | Single-Layer Perceptron Neural Network | Advanced | [project_085_single_layer_perceptron_neural_network.py](projects/project_085_single_layer_perceptron_neural_network.py) |
| 86 | Decision Tree Binary Rule Classifier | Advanced | [project_086_decision_tree_binary_rule_classifier.py](projects/project_086_decision_tree_binary_rule_classifier.py) |
| 87 | Optical Character Recognition (OCR) 8x8 Grid Matcher | Intermediate | [project_087_optical_character_recognition_ocr_8x8_gr.py](projects/project_087_optical_character_recognition_ocr_8x8_gr.py) |
| 88 | Convolutional Image Filter & Edge Detector | Advanced | [project_088_convolutional_image_filter_edge_detector.py](projects/project_088_convolutional_image_filter_edge_detector.py) |
| 89 | Dimensionality Reduction Engine (PCA Simulation) | Intermediate | [project_089_dimensionality_reduction_engine_pca_simu.py](projects/project_089_dimensionality_reduction_engine_pca_simu.py) |
| 90 | Multi-Layer Feedforward Neural Network | Advanced | [project_090_multi_layer_feedforward_neural_network.py](projects/project_090_multi_layer_feedforward_neural_network.py) |

### Section 10: Full-Stack Capstone Systems & Architectures

| # | Project | Level | File |
|---|---|---|---|
| 91 | Enterprise Point-of-Sale (POS) & Retail Billing Terminal | Advanced | [project_091_enterprise_point_of_sale_pos_retail_bill.py](projects/project_091_enterprise_point_of_sale_pos_retail_bill.py) |
| 92 | Distributed API Gateway & Load Balancer | Advanced | [project_092_distributed_api_gateway_load_balancer.py](projects/project_092_distributed_api_gateway_load_balancer.py) |
| 93 | Automated E-Commerce Order Processing Pipeline | Advanced | [project_093_automated_e_commerce_order_processing_pi.py](projects/project_093_automated_e_commerce_order_processing_pi.py) |
| 94 | Continuous Integration (CI) Test Runner Bot | Advanced | [project_094_continuous_integration_ci_test_runner_bo.py](projects/project_094_continuous_integration_ci_test_runner_bo.py) |
| 95 | Cryptographic File Sync & Mirroring Daemon | Advanced | [project_095_cryptographic_file_sync_mirroring_daemon.py](projects/project_095_cryptographic_file_sync_mirroring_daemon.py) |
| 96 | Network Traffic & Socket Packet Analyzer | Advanced | [project_096_network_traffic_socket_packet_analyzer.py](projects/project_096_network_traffic_socket_packet_analyzer.py) |
| 97 | Full-Stack Web CMS & Dynamic Content Renderer | Advanced | [project_097_full_stack_web_cms_dynamic_content_rende.py](projects/project_097_full_stack_web_cms_dynamic_content_rende.py) |
| 98 | Event-Driven Micro-Broker & Pub/Sub Message Bus | Advanced | [project_098_event_driven_micro_broker_pub_sub_messag.py](projects/project_098_event_driven_micro_broker_pub_sub_messag.py) |
| 99 | IT Infrastructure Monitoring & Alerting Hub | Advanced | [project_099_it_infrastructure_monitoring_alerting_hu.py](projects/project_099_it_infrastructure_monitoring_alerting_hu.py) |
| 100 | Autonomous Self-Healing System Supervisor & Watchdog | Advanced | [project_100_autonomous_self_healing_system_superviso.py](projects/project_100_autonomous_self_healing_system_superviso.py) |

## About the author

Anuj Kumar Saxena - educator, software engineer and programming writer. Contact: anujrampur@gmail.com

## Copyright

Copyright (c) 2026 Anuj Kumar Saxena. The code is provided for readers of the book, for learning and personal projects. If you want to allow wider reuse, add a LICENSE file (for example MIT) to this repository.
