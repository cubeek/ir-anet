config:
  plugin_type: install
subparsers:
  # the actual name of the plugin
  vqfx:
    description: The plugin sets up a virtual Juniper QFX switch
    include_groups: ["Ansible options", "Common options"]
    groups:
      - title: I don't know what is this for
        options:
          configure_nested:
            type: Bool
            help: Whether nested virtualization should be enabled on this host.
            default: False
          ovs_bridges:
            type: Value
            help: List of OVS bridges to set up.
            default: dunno how to make a list
