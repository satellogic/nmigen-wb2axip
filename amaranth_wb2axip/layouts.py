from amaranth.hdl.rec import DIR_FANIN, DIR_FANOUT

def to_direction(interface, d):
    assert interface in ['master', 'slave']
    assert d in ['m_to_s', 's_to_m']

    if interface == 'master':
        return DIR_FANOUT if d == 'm_to_s' else DIR_FANIN
    else:
        return DIR_FANOUT if d == 's_to_m' else DIR_FANIN

def get_axilite_layout(interface, data_w, addr_w):
    assert interface in ['master', 'slave']
    layout = [
		('ARADDR', addr_w, 'm_to_s'),
		('ARPROT', 3, 'm_to_s'),
		('ARREADY', 1, 's_to_m'),
		('ARVALID', 1, 'm_to_s'),
		('AWADDR', addr_w, 'm_to_s'),
		('AWPROT', 3, 'm_to_s'),
		('AWREADY', 1, 's_to_m'),
		('AWVALID', 1, 'm_to_s'),
		('BREADY', 1, 'm_to_s'),
		('BRESP', 2, 's_to_m'),
		('BVALID', 1, 's_to_m'),
		('RDATA', data_w, 's_to_m'),
		('RREADY', 1, 'm_to_s'),
		('RRESP', 2, 's_to_m'),
		('RVALID', 1, 's_to_m'),
		('WDATA', data_w, 'm_to_s'),
		('WREADY', 1, 's_to_m'),
		('WSTRB', data_w // 8, 'm_to_s'),
		('WVALID', 1, 'm_to_s'),
    ]
    return [(f, w, to_direction(interface, d)) for f, w, d in layout]

def get_axi_layout(interface, data_w, addr_w, id_w, user_w):
    assert interface in ['master', 'slave']
    layout = [
        ("ARADDR", addr_w, "m_to_s"),
        ("ARBURST", 2, "m_to_s"),
        ("ARCACHE", 4, "m_to_s"),
        ("ARID", id_w, "m_to_s"),
        ("ARLEN", 8, "m_to_s"),
        ("ARLOCK", 1, "m_to_s"),
        ("ARPROT", 3, "m_to_s"),
        ("ARQOS", 4, "m_to_s"),
        ("ARREADY", 1, "s_to_m"),
        ("ARSIZE", 3, "m_to_s"),
        ("ARUSER", user_w, "m_to_s"),
        ("ARVALID", 1, "m_to_s"),
        ("AWADDR", addr_w, "m_to_s"),
        ("AWBURST", 2, "m_to_s"),
        ("AWCACHE", 4, "m_to_s"),
        ("AWID", id_w, "m_to_s"),
        ("AWLEN", 8, "m_to_s"),
        ("AWLOCK", 1, "m_to_s"),
        ("AWPROT", 3, "m_to_s"),
        ("AWQOS", 4, "m_to_s"),
        ("AWREADY", 1, "s_to_m"),
        ("AWSIZE", 3, "m_to_s"),
        ("AWUSER", user_w, "m_to_s"),
        ("AWVALID", 1, "m_to_s"),
        ("BID", id_w, "s_to_m"),
        ("BREADY", 1, "m_to_s"),
        ("BRESP", 2, "s_to_m"),
        ("BVALID", 1, "s_to_m"),
        ("RDATA", data_w, "s_to_m"),
        ("RID", id_w, "s_to_m"),
        ("RLAST", 1, "s_to_m"),
        ("RREADY", 1, "m_to_s"),
        ("RRESP", 2, "s_to_m"),
        ("RVALID", 1, "s_to_m"),
        ("WDATA", data_w, "m_to_s"),
        ("WLAST", 1, "m_to_s"),
        ("WREADY", 1, "s_to_m"),
        ("WSTRB", data_w // 8, "m_to_s"),
        ("WVALID", 1, "m_to_s"),
    ]
    return [(f, w, to_direction(interface, d)) for f, w, d in layout if w > 0]
