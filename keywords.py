from ClusteringAlgorithms.string_tools import new_extended_list

# primary keywords
general_keywords = ['CVE', 'exploit', '0day', '0-day', 'zero-day', 'exploitdb']
primary_program_names = ['openssl', 'mysql', 'postgresql']
primary_attack_types = ['shellcode', 'shellshock', 'csrf', 'backdoor', 'cross-site', 'xss', 'overflow', 'sql'
                        'unauthenticated', 'metasploit', 'escalation']

# secondary keywords
secondary_general_keywords = ['patch', 'vulnerability', 'security', 'threat', 'vulnerabilities', 'denial', 'service']
secondary_program_names = ['windows', 'office', 'php', 'javascript', 'adobe', 'flash', 'windows', 'wordpress', 'cisco']
secondary_attack_types = ['privilege', 'directory', 'traversal', 'buffer', 'file', 'disclosure', 'bypass', 'command',
                          'sql', 'injection']
miscellaneous = ['root', 'rootkit', 'kit', 'credential', 'credentials', 'unauthorized', 'remote',
                 'execution', 'hacked', 'bypass']

primary_keywords = new_extended_list(general_keywords, primary_program_names, primary_attack_types)
program_names = new_extended_list(primary_program_names, secondary_program_names)
attack_types = new_extended_list(primary_attack_types, secondary_attack_types)
all_keywords = new_extended_list(primary_keywords, secondary_attack_types, secondary_program_names,
                                 secondary_general_keywords, miscellaneous)
