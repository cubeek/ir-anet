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
          ovs_bridge:
            type: Value
            help: OVS bridges that connects nodes with virtual switch.
            default: br-vqfx
