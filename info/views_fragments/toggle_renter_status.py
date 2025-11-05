def toggle_renter_status(request, renter_id):
    # Get the renter instance
    renter = Renter.objects.get(id=renter_id)
    if renter.user:
        # Toggle the active status
        renter.user.is_active = not renter.user.is_active
        renter.user.save()
        
        action = "kích hoạt" if renter.user.is_active else "khóa"
        messages.success(request, f"Đã {action} tài khoản của {renter.hoten}")
    else:
        messages.error(request, f"Người thuê {renter.hoten} chưa có tài khoản")
    
    return redirect('renter_list')