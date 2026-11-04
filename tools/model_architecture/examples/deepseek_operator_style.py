"""Operator-only presentation inspired by deepseek_v4_architecture.jpg.

Preserve full source annotations in description; never infer new computation.
"""

MAIN={
 'title':'DeepSeek-V4-Flash (284B / 13B active)',
 'subtitle':'43 layers · hidden 4096 · Q 64 / KV 1 · context 1M',
 'defaults':'256 experts · top-6 + 1 shared · head dim 512 · window 128',
 'mhc_heading':'mHC','compress_heading':'Compressor — CSA / HCA','main_heading':'Transformer ×43',
 'attention_heading':'CSA / HCA / SWA','moe_heading':'MoE / MLP','indexer_heading':'Lightning Indexer (CSA only)',
 'hc_x':'X [4,4096]','hc_flat':'RMSNorm','hc_linear':'Linear → Scale + Bias',
 'hc_pre':'Sigmoid\n+ ε','hc_post':'2 × Sigmoid','hc_comb':'Reshape\n[4,4]',
 'hc_soft':'Softmax','hc_sink':'Sinkhorn\n×20','hc_collapse':'Σ preᵢXᵢ','hc_norm':'RMSNorm',
 'hc_fun':'Attention / MoE','hc_expand':'post × F(h)','hc_residual':'combᵀ × X','hc_sum':'+','hc_y':'X′ [4,4096]',
 'hc_note':'pre / post / comb ← X',
 'main_tokens':'Token IDs','main_embed':'Embedding','main_streams':'Repeat ×4','main_layer_x':'X [4,4096]',
 'main_attn_pre':'hc_pre','main_attn_norm':'RMSNorm','main_attn_core':'CSA / HCA / SWA',
 'main_attn_mix':'hc_post + Residual','main_ffn_pre':'hc_pre','main_ffn_norm':'RMSNorm',
 'main_ffn':'Hash-MoE / MoE','main_ffn_mix':'hc_post + Residual','main_layer_y':'Decoder ×43',
 'main_hyperhead':'HC-head','main_norm':'RMSNorm','main_head':'LM-head','main_output':'Logits [129280]',
 'schedule':'L0–1: SWA\nL2–41: [CSA4, HCA128] ×20\nL42: CSA4\nHash-MoE: L0–2',
 'attn_x':'h [4096]','attn_qa':'Linear (Q down)','attn_qan':'RMSNorm','attn_qb':'Linear (Q up)',
 'attn_qn':'Q head Norm','attn_qrope':'RoPE₆₄','attn_kv':'Linear (KV down)',
 'attn_kvn':'RMSNorm','attn_kvrope':'RoPE₆₄','attn_kvquant':'Quant (FP8 sim)',
 'attn_local':'KV cache (window)\nK and V are the SAME',
 'attn_compressor':'Compressor\nC4 / C128','attn_entries':'KV cache (compress)',
 'attn_mask':'CSA: TopK + Mask\nHCA: Causal Mask','attn_concat':'Concat (KV)',
 'attn_core':'Attention (MQA)','attn_sink':'sink','attn_inverse':'RoPE (inverse)',
 'attn_oa':'Linear (O down)\n8 × [4096→1024]','attn_ob':'Linear (O up)\n8192→4096','attn_y':'h′ [4096]',
 'csa_label':'CSA (C4)','hca_label':'HCA (C128)',
 'moe_x':'h [4096]','moe_shared':'Shared MLP ×1','moe_router':'Linear → √Softplus\nHash / Top6',
 'moe_weights':'Gather → Normalize\n×1.5','moe_bank':'MLP ×256\n6 active','moe_sum':'Σ weighted experts',
 'moe_add':'+','moe_y':'h′ [4096]','expert_x':'x [4096]',
 'expert_up':'Linear (up)\nClip [−10,10]','expert_gate':'Linear (gate)\nClip max10 → SiLU',
 'expert_mul':'×','expert_weight':'× routing weight','expert_down':'Linear (down)','expert_y':'y [4096]',
 'moe_note':'Hash L0–2 · Learned Top6 L3–42',
 'idx_q':'Qr [1024]','idx_qproj':'Linear → RoPE\nHadamard → Quant',
 'idx_key':'Compressor C4\ndim 128','idx_kcache':'Norm → RoPE → Rotate → Quant\nKV cache (index)',
 'idx_h':'Linear (weights)','idx_score':'Matmul → ReLU → Scale → Sum',
 'idx_select':'Mask → TopK (≤512)','idx_note':'Q / K quantization: FP4 simulation',
 'mtp_heading':'MTP (auxiliary)','mtp_h':'Hidden streams','mtp_hn':'RMSNorm (h)',
 'mtp_hp':'Linear (h)','mtp_e':'Shared Embedding','mtp_en':'RMSNorm (e)',
 'mtp_ep':'Linear (e)','mtp_sum':'+','mtp_block':'Block L43 (SWA)',
 'mtp_head':'HC-head → Norm → LM-head',
 'footer':'Official Flash checkpoint 60d8d707 · detailed evidence: README / evidence.md · no GPU inference',
}
for k,r in [('csa',4),('hca',128)]:
 MAIN.update({k+'_x':'h [4096]',k+'_kv':'Linear (KV proj)',k+'_gate':'Linear (Gate proj)',
 k+'_window':('Cat (prev Ca, cur Cb)\nwindow 8 / stride 4' if r==4 else 'Window 128\nstride 128'),
 k+'_bias':'+ APE → Softmax',k+'_sum':'× → Sum',k+'_norm':'RMSNorm',k+'_rope':'RoPE₆₄',
 k+'_quant':'Quant → KV cache',k+'_out':('Indexer → TopK' if r==4 else 'Causal Mask\nNO indexer')})

DETAIL={
 'source':'hidden 4096 · heads 64 · head dim 512 · window 128',
 'ports':'A: compressed KV     I: compressed indices     Qr: normalized low-rank query',
 'compressor_title':'Compressor','middle_title':'Indexer','attention_title':'Attention (MQA)',
 'comp_h':'h [4096]','comp_fp32':'Cast FP32','comp_wkv':'Linear (KV proj)',
 'comp_wgate':'Linear (Gate proj)','comp_split':'Split (Ca / Cb)',
 'comp_ape':'+ APE','comp_gate_split':'Split (Za / Zb)',
 'comp_value_window':'Cat (prev Ca, cur Cb)','comp_gate_window':'Cat (prev Za, cur Zb)',
 'comp_softmax':'Softmax (tokens)','comp_mul':'×','comp_sum':'Sum (tokens)',
 'comp_complete':'Stride boundary','comp_norm':'RMSNorm','comp_nope':'Quant (FP8 sim)\ncontent 448',
 'comp_rope':'RoPE₆₄','comp_concat':'Concat','comp_write':'Cache Write',
 'comp_bank':'KV cache (compress)','comp_alias':'View [:,128:]','port_A':'A: KV [Nc,512]',
 'comp_note':'KV / Gate are independent projections',
 'idx_q_input':'Qr [1024]','idx_h':'h [4096]','idx_q_proj':'Linear (Q up)',
 'idx_q_heads':'Reshape\n[64,128]','idx_q_rope':'RoPE₆₄','idx_q_hadamard':'Rotate (Hadamard)',
 'idx_q_fp4':'Quant (FP4 sim)','idx_q_ready':'Qᵢ [64,128]',
 'idx_kv_proj':'Linear\n(KV)','idx_gate_proj':'Linear\n(Gate)','idx_w_proj':'Linear (weights)',
 'idx_kv_split':'Split\nCa / Cb','idx_gate_ape':'+ APE\nSplit Za / Zb',
 'idx_window':'Cat (prev, current)\n8 × 128','idx_softmax':'Softmax (tokens)',
 'idx_pool':'× → Sum','idx_norm':'RMSNorm','idx_key_rope':'RoPE₆₄',
 'idx_key_hadamard':'Rotate (Hadamard)','idx_key_fp4':'Quant (FP4 sim)',
 'idx_key_cache':'KV cache (index)\n[Nc,128]','idx_w_scale':'Scale\n128⁻½ × 64⁻½',
 'idx_w_ready':'weights [64]','idx_dot':'Matmul (Qᵢ, Kᵢᵀ)','idx_relu':'ReLU',
 'idx_head_sum':'Scale → Sum (heads)','idx_tp':'AllReduce (TP)',
 'idx_causal':'Causal Mask','idx_topk':'TopK (≤512)','port_I':'I: compressed indices',
 'hca_no_indexer':'Position indices · NO Indexer',
 'hist_prefill_input':'Prefill: t ∈ [0,T)','hist_prefill_nc':'Nc = ⌊T/128⌋',
 'hist_prefill_range':'Arange (Nc)','hist_prefill_threshold':'visible = ⌊(t+1)/128⌋',
 'hist_prefill_mask':'Causal Mask (−1)','hist_prefill_offset':'+ T','hist_prefill_expand':'Expand [B,T,Nc]',
 'hist_decode_input':'Decode: position p','hist_decode_nc':'Nc = ⌊(p+1)/128⌋',
 'hist_decode_range':'Arange (Nc)','hist_decode_threshold':'Valid prefix',
 'hist_decode_mask':'All eligible indices','hist_decode_offset':'+ 128','hist_decode_expand':'Expand [B,1,Nc]',
 'hist_mode':'Select (prefill / decode)','hist_valid':'128(j+1) ≤ t+1',
 'hist_no_prune':'Nc(t)=floor((t+1)/128)',
 'hist_examples':'t=127 → j0\nt=255 → j0,j1',
 'hist_storage':'A: KV cache (compress)','hist_port_type':'Cast int32',
 'attn_h':'h [4096]','attn_qa':'Linear (Q down)\n4096→1024','attn_qrank':'RMSNorm → Qr',
 'attn_qb':'Linear (Q up)\n1024→64×512','attn_qhead':'Q head Norm',
 'attn_qrope':'RoPE₆₄','attn_qready':'Q [64,512]',
 'attn_wkv':'Linear (KV down)\n4096→512','attn_kvnorm':'RMSNorm',
 'attn_kvrope':'RoPE₆₄','attn_kvquant':'Quant (FP8 sim)',
 'attn_ring':'KV cache (window)\n128 × 512','attn_positions':'Position (t / p)',
 'attn_win_indices':'Window indices (128)','attn_I':'I: compressed indices',
 'attn_A':'A: compressed KV','attn_bank':'Concat (window KV, compressed KV)',
 'attn_indices':'Concat (window indices, I)',
 'attn_gather':'Gather (KV) → QKᵀ / √512','attn_softmax':'Softmax (+ sink)',
 'attn_sink':'sink','attn_values':'Matmul (P, V)',
 'attn_inverse':'RoPE (inverse)','attn_oa':'Linear (O down)\n8 groups × (4096→1024)',
 'attn_ob':'Linear (O up)\n8192→4096','attn_output':'h′ [4096]',
 'states_title':'kv_state / score_state',
 'state_shapes':'kv_state / score_state','state_prefill':'Prefill → Buffer remainder',
 'state_decode':'Decode → Update slot',
 'state_window1':'prev Ca [4,512]','state_window2':'cur Cb [4,512]',
 'state_move':'prev ← current (on stride boundary)',
 'footer':'Official Flash @ 60d8d707 · FP4 / FP8 = simulation · source details: operator_notes.md',
}

def apply(g,kind='overview'):
    labels=dict(MAIN if kind=='overview' else DETAIL)
    if kind!='overview':
        r=4 if kind=='csa' else 128
        labels.update(title=f'DeepSeek-V4-Flash — {kind.upper()}',
          facts=f'{kind.upper()} · stride {r} · '+('window 8 · index dim 128 · top-k ≤512' if r==4 else 'window 128 · all causal compressed entries'),
          state_shapes=f'kv_state / score_state\n[{8 if r==4 else 128},{1024 if r==4 else 512}]',
          state_decode=f'Update → Emit every {r} tokens')
        if kind=='hca':labels.update(middle_title='Causal indices',comp_split='Reshape [128,512]',
          comp_gate_split='Reshape [128,512]',comp_value_window='KV window [128,512]',
          comp_gate_window='Gate window [128,512]',state_window1='Tokens 0…127 → KV₀',
          state_window2='Tokens 128…255 → KV₁',state_move='Append one KV every 128 tokens',
          attn_qrank='RMSNorm',ports='A: compressed KV     I: causal compressed indices')
    g['presentation']={'reference':'models/deepseek_v4/deepseek_v4_architecture.jpg',
      'style':'operator blocks; colored modules; dashed frames; bottom-up',
      'notes':'Full annotations preserved in description and operator_notes.md; Flash parameters retained.'}
    # Compress only vertical geometry; preserve every branch/waypoint and aligned port.
    sy=.6
    g['height']=round(g['height']*sy)
    for e in g['edges']:
        if 'points' in e:e['points']=[[x,y*sy] for x,y in e['points']]
    for n in g['nodes']:
        key=n['id'];original=n['label'];n['description']=original
        if original and key not in labels:raise ValueError('Missing concise operator label: '+key)
        n['label']=labels.get(key,'')
        x,y,w,h=n['box'];n['box']=[x,y*sy,w,h*sy]
        decorative=n.get('kind')=='decoration'
        is_frame=decorative and not original
        if kind=='overview':
            color=('#7f8cff' if key.startswith(('hc_','main_','mtp_')) else
                   '#91cc48' if key.startswith(('idx_','expert_')) else
                   '#ff9f14' if key.startswith(('attn_','csa_')) else
                   '#399e90' if key.startswith('hca_') else
                   '#48c9b9' if key.startswith('moe_') else '#7f8cff')
        else:
            color=('#91cc48' if key.startswith(('idx_','hist_')) or key in ['port_I','middle_title'] else
                   '#ff9f14' if key.startswith('attn_') and kind=='csa' else
                   '#399e90' if key.startswith('attn_') else '#8797fa')
        cache=('cache' in n['label'].lower() and key not in ['comp_write'])
        if cache:color='#ed343b'
        font=24 if kind!='overview' else 19
        if key=='title':font=34
        # Fit compact labels with at most two lines in almost all operation blocks.
        lines=n['label'].split('\n')
        while font>12 and (len(lines)*font*1.2+10>h*sy or max(map(len,lines),default=0)*font*.57+16>w):font-=1
        framecolor=color
        n['style']=(f'rounded=1;arcSize=10;absoluteArcSize=1;whiteSpace=wrap;html=0;'
          f'fontFamily=Arial;fontSize={font};fontColor=#ffffff;align=center;verticalAlign=middle;'
          f'spacing=4;strokeColor={color};strokeWidth=1;fillColor={color};')
        if is_frame:n['style']+=f'fillColor=none;dashed=1;dashPattern=7 5;strokeColor={framecolor};'
        elif decorative:n['style']+='fillColor=none;strokeColor=none;fontColor=#233247;fontStyle=1;'
        if n['label'] in ['+','×']:
            # Compact arithmetic junctions, like the reference diagram.
            side=h*sy
            n['box']=[x+(w-side)/2,y*sy,side,side]
            n['style']+='shape=ellipse;perimeter=ellipsePerimeter;fontSize=22;fontStyle=1;'
    return g
